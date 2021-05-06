import json
import datetime
import calendar
from dateutil.relativedelta  import relativedelta

from django.http      import JsonResponse
from django.shortcuts import render
from django.views     import View
from django.db.models import F, IntegerField
from django.db.models.expressions import Window
from django.db.models.functions   import FirstValue, ExtractDay, Cast, TruncMonth
from django.db.models.aggregates  import Max, Min, Sum

from .serializers import StockPriceSerializer
from .models import StockPrice, Ticker

from stock.stock_price_crawler import get_current_price
from utils.error_handlers import handle_candle_chart_input_error


class StockPriceView(View):
    def get(self, request):
        return render(request, 'stock/index.html', {})


class CurrentStockPriceView(View):
    def get(self, request):
        ticker        = request.GET.get('ticker')
        current_price, open_price = get_current_price(ticker)

        if isinstance(current_price, bool):
            if current_price == False:
                error_msg = open_price
                return error_msg

        return current_price


class StockCandleChart(View):
    def get(self, request):
        chart_type  = request.GET.get('chart_type', 'daily')
        code        = request.GET.get('ticker', None)

        error_handler_res = handle_candle_chart_input_error(chart_type, code)
        if isinstance(error_handler_res, JsonResponse):
            return error_handler_res

        two_years_from_now = datetime.datetime.now() - relativedelta(years=2)
        
        ticker          = Ticker.objects.get(code=code)
        stock_prices_qs = StockPrice.objects.filter(ticker=ticker, date__gte=two_years_from_now)

        filtered_stock_prices_qs = self.get_candle_chart_by_type(chart_type, stock_prices_qs)

        serializer   = StockPriceSerializer(filtered_stock_prices_qs, many=True)
        stock_prices = serializer.data

        data = {
                'name'  : ticker.stock_name,
                'ticker': ticker.code,
                'values': stock_prices
            }
        return JsonResponse({'results': data}, status=200)

    def get_candle_chart_by_type(self, chart_type, stock_prices_qs):
        if chart_type == 'daily':
            results_qs = stock_prices_qs.values('date', 'bprc_adj', 'prc_adj', 'hi_adj', 'lo_adj', 'volume').order_by('date')
            return list(results_qs)

        if chart_type == 'weekly':
            today       = datetime.datetime.today()
            this_friday = today + datetime.timedelta((calendar.FRIDAY - today.weekday()) % 7)
            base_date   = this_friday.date()

            first_qs = stock_prices_qs.annotate(group_id=Cast(
                                        ExtractDay(base_date - F('date')), IntegerField()) / 7).order_by('date')
        elif chart_type == 'monthly':
             first_qs = stock_prices_qs.annotate(group_id=TruncMonth(F('date'))).order_by('date')

        second_qs = first_qs.values('group_id')\
                            .annotate(
                                    bprc_adj=Window(
                                        expression   = FirstValue('bprc_adj'),
                                        partition_by = F('group_id'),
                                        order_by     = F('date').asc()
                                    ),
                                    prc_adj=Window(
                                        expression   = FirstValue('prc_adj'),
                                        partition_by = F('group_id'),
                                        order_by     = F('date').desc()
                                    ),
                                    date=Window(
                                        expression   = Max('date'),
                                        partition_by = F('group_id')
                                    ),
                                    hi_adj=Window(
                                        expression   = Max('hi_adj'),
                                        partition_by = F('group_id')
                                    ),
                                    lo_adj=Window(
                                        expression   = Min('lo_adj'),
                                        partition_by = F('group_id')
                                    ),
                                    volume=Window(
                                        expression   = Sum('volume'),
                                        partition_by = F('group_id')
                                    )
                            )\
                            .distinct('date')\
                            .values('date', 'bprc_adj', 'prc_adj', 'hi_adj', 'lo_adj', 'volume')
        results = list(second_qs)
        return results
