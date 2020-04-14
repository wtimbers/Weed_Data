#!/usr/bin/env python3
from datetime import datetime
import csv
import matplotlib.pyplot as plt
plt.style.use('seaborn')
import sys

def main():
	print(datetime.now())

	print("\nTotal:")
	print("{} times since I first got high in June 2010".format(total_sum(raw_data)))

	print("\nOverall Averages:")
	print("{} times per month\n{} times per week\n{} days per time".format(monthly_avg(raw_data), weekly_avg(raw_data), days_per_time(raw_data)))

	print("\n---")
	print("\nYearly Trends:")
	all_years_at_once()
	print()
	compare_years()

	print("\n---")
	print("\nMonthly Trends:")
	all_months_at_once()
	print()
	compare_months()

	print("\n---")
	print("\nSeasonal Trends:")
	all_seasons_at_once()
	print()
	compare_seasons()

	print("\n---")
	print("\nHighest Frequency Periods:")
	print(highest_density_months(raw_data, 24))
	print(highest_density_months(raw_data, 12))
	print(highest_density_months(raw_data, 6))
	print(highest_density_months(raw_data, 3))
	print(highest_density_months(raw_data, 1))

	print("\nLowest Frequency Periods:")
	print(lowest_density_months(raw_data, 24))
	print(lowest_density_months(raw_data, 12))
	print(lowest_density_months(raw_data, 6))
	print(lowest_density_months(raw_data, 3))
	print(lowest_density_months(raw_data, 1))

	print("\n---")
	print("\nDuring College:")
	print(print_range_data(raw_data, "June 2010", "May 2013"))

	print("\nSummer Before Sophomore Year:")
	print(print_range_data(raw_data, "April 2011", "August 2011"))

	print("\nSince College:")
	print(print_range_data(raw_data, "June 2013", convert_date(datetime.now())))

	print("\nLiving At Home:")
	print(print_range_data(raw_data, "June 2013", "November 2018"))

	print("\nLiving at Josh's:")
	print(print_range_data(raw_data, "November 2018", convert_date(datetime.now())))

	print("\nSince weed became legal in CO:")
	print(print_range_data(raw_data, "January 2014", convert_date(datetime.now())))

	print("\nVaporFi Orbit Vaporizer Era:")
	print(print_range_data(raw_data, "December 2015", "October 2018"))

	print("\nDaVinci Miqro Vaporizer Era:")
	print(print_range_data(raw_data, "November 2019", convert_date(datetime.now())))
	
	#flush (?) system to print data before plotting graphs
	sys.stdout.flush()

	make_bar("All-Time Data", "Months", "Times", raw_data, "yes", 3, 80)
	make_bar("Monthly Averages by Year", "Year", "Monthly Averages", years_monthly_avg_dict(yearly_data_dict), "yes", 1, 0)
	make_bar("Monthly Averages by Month", "Month", "Monthly Averages", months_monthly_avg_dict(raw_data), "no", 1, 60)
	make_bar("Monthly Averages by Season", "Season", "Monthly Averages", seasons_monthly_avg_dict(raw_data), "no", 1, 60)


# Pulls in frequency numbers from csv file and forms a list for the year
def freq_lists(year):
	freq_list = []
	with open('/Users/Will/Google Drive File Stream/My Drive/Personal/Weed_Data/Raw Data/weed_data.csv') as weed_csv:
		weed_csv_reader = csv.DictReader(weed_csv)
		for row in weed_csv_reader:
			freq_list.append(row["{}".format(year)])
		freq_list = [int(i) for i in freq_list if i != ""]
	return freq_list

# Converts datetime object to string, correcting for lack of data for current month
def convert_date(date):
	if date.year == datetime.now().year and date.month == datetime.now().month:
		month = date.month - 1
		new_date = datetime(date.year, month, 1)
		return datetime.strftime(new_date, "%B %Y")
	else:
		return datetime.strftime(date, "%B %Y")

# Converts string to datetime object
def convert_string(date):
	return datetime.strptime(date, "%B %Y")

# Creates a list of month and year pairs for a year
def date_increment(year):
	end_year = year + 1
	month_list = []
	if year == 2010:
		month = 6
	else:
		month = 1
	while end_year > year:
		month_list.append(convert_date(datetime(year, month, 1)))
		if month == 12:
			year += 1
		else:
			month +=1
		if year == datetime.now().year:
			if month == datetime.now().month:
				break
	return month_list


def zip_list(year):
	return dict(zip(date_increment(year), freq_lists(year)))

def unpack(crazy_list):
	new_dict = {}
	for dict in crazy_list:
		new_dict.update(**dict)
	return new_dict

yearly_data_dict = [zip_list(i) for i in range(2010, datetime.now().year + 1)]
raw_data = unpack(yearly_data_dict)


'''Determines the chosen number of consecutive months with the highest frequency of getting high, 
plus the number of times getting high, not restricted to calendar year'''
def highest_density_months(data, month_span):
	max_list = []
	month_range = []
	for month, num in data.items():
		if len(max_list) < month_span:
			max_list.append(num)
			month_range.append(month)
			test_list = max_list
			test_range = month_range
		elif len(max_list) == month_span:
			test_list = test_list[1:]
			test_list.append(num)
			test_range = test_range[1:]
			test_range.append(month)
			if sum(test_list) >= sum(max_list):
				max_list = test_list
				month_range = test_range
	grand_total = sum(max_list)
	new_dict = {month_range[i]: max_list[i] for i in range(len(month_range))}
	if len(month_range) == 1:
		return '''{grand_total} in {month_span} month in {one_month}
   Avgs for period: monthly = {month} | weekly = {week} | days / time = {days}
           Compare: monthly = {month_diff} | weekly = {week_diff} | days / time = {day_diff} \
   '''.format(month_span=month_span, one_month=month_range[0], grand_total=grand_total, month=monthly_avg(new_dict), week=weekly_avg(new_dict), days=days_per_time(new_dict), month_diff=compare_avg("monthly", new_dict), week_diff=compare_avg("weekly", new_dict), day_diff=compare_avg("daily", new_dict))
	else:
		return '''{grand_total} times in {month_span}-month span from {first_month} to {last_month}
   Avgs for period: monthly = {month} | weekly = {week} | days / time = {days}
           Compare: monthly = {month_diff} | weekly = {week_diff} | days / time = {day_diff} \
   '''.format(month_span=month_span, first_month=month_range[0], last_month=month_range[-1], grand_total=grand_total, month=monthly_avg(new_dict), week=weekly_avg(new_dict), days=days_per_time(new_dict), month_diff=compare_avg("monthly", new_dict), week_diff=compare_avg("weekly", new_dict), day_diff=compare_avg("daily", new_dict))

'''Determines the chosen number of consecutive months with the lowest frequency of getting high, 
plus the number of times getting high, not restricted to calendar year'''
def lowest_density_months(data, month_span):
	max_list = []
	month_range = []
	for month, num in data.items():
		if len(max_list) < month_span:
			max_list.append(num)
			month_range.append(month)
			test_list = max_list
			test_range = month_range
		elif len(max_list) == month_span:
			test_list = test_list[1:]
			test_list.append(num)
			test_range = test_range[1:]
			test_range.append(month)
			if sum(test_list) <= sum(max_list):
				max_list = test_list
				month_range = test_range
	grand_total = sum(max_list)
	new_dict = {month_range[i]: max_list[i] for i in range(len(month_range))}
	if len(month_range) == 1:
		return '''{grand_total} in {month_span} month in {one_month}
   Avgs for period: monthly = {month} | weekly = {week} | days / time = {days}
           Compare: monthly = {month_diff} | weekly = {week_diff} | days / time = {day_diff} \
   '''.format(month_span=month_span, one_month=month_range[0], grand_total=grand_total, month=monthly_avg(new_dict), week=weekly_avg(new_dict), days=days_per_time(new_dict), month_diff=compare_avg("monthly", new_dict), week_diff=compare_avg("weekly", new_dict), day_diff=compare_avg("daily", new_dict))
	else:
		return '''{grand_total} times in {month_span}-month span from {first_month} to {last_month}
   Avgs for period: monthly = {month} | weekly = {week} | days / time = {days}
           Compare: monthly = {month_diff} | weekly = {week_diff} | days / time = {day_diff} \
   '''.format(month_span=month_span, first_month=month_range[0], last_month=month_range[-1], grand_total=grand_total, month=monthly_avg(new_dict), week=weekly_avg(new_dict), days=days_per_time(new_dict), month_diff=compare_avg("monthly", new_dict), week_diff=compare_avg("weekly", new_dict), day_diff=compare_avg("daily", new_dict))

# Takes a dictionary
def total_sum(data):
	return sum(data.values())

# Takes a dictionary, returns the monthly average
def monthly_avg(data):
	per_month = round(sum(data.values()) / len(data), 1)
	return per_month

# Takes a dictionary
def weekly_avg(data):
	per_week = round(sum(data.values()) / (len(data) * 4.33333333333), 1)
	return per_week

# Takes a dictionary
def days_per_time(data):
	try:
		per_time = round((len(data) * 30.41666667) / total_sum(data), 1)
		return per_time
	except ZeroDivisionError:
		return "N/A"

# Receives an average type and a dictionary and compares the requested average to the raw data
def compare_avg(avg_type, compare_data):
	if avg_type == "monthly":
		result = round(monthly_avg(compare_data)-monthly_avg(raw_data), 1)
	elif avg_type == "weekly":
		result = round(weekly_avg(compare_data)-weekly_avg(raw_data), 1)
	elif avg_type == "daily":
		try:
			result = round(days_per_time(compare_data)-days_per_time(raw_data), 1)
		except:
			result = "N/A"
	if result == "N/A":
		return result
	elif result > 0:
		return "+" + str(result)
	else:
		return result


year_list = [i for i in range(2010, datetime.now().year + 1)]

''' takes the yearly_data_dict (dict of year lists) and a specific year
and returns the dict from that year as well as the total number of times '''
def yearly_trends(data, year):
	index = year - 2010
	year_dict = data[index]
	total = 0
	for month, num in year_dict.items():
		total += num
	return total, year_dict

def print_yearly_trends(data, year):
	total, year_dict = yearly_trends(data, year)
	return '''{total} times for {year}
   Avgs for year: monthly = {monthly} | weekly = {week} | days / time = {days}
         Compare: monthly = {month_diff} | weekly = {week_diff} | days / time = {day_diff} \
   '''.format(total=total, year=year, monthly=monthly_avg(year_dict), week=weekly_avg(year_dict), days=days_per_time(year_dict), month_diff=compare_avg("monthly", year_dict), week_diff=compare_avg("weekly", year_dict), day_diff=compare_avg("daily", year_dict))

# Calls functions for yearly trend analysis and prints for each year from 2010 until current year
def all_years_at_once():
	for year in year_list:
		print(print_yearly_trends(yearly_data_dict, year))

def compare_years():
	test_max = float("-inf")
	test_min = float("inf")
	for year in year_list:
		total, year_dict = yearly_trends(yearly_data_dict, year)
		if monthly_avg(year_dict) > test_max:
			test_max = monthly_avg(year_dict)
			highest_year = year
		if monthly_avg(year_dict) < test_min:
			test_min = monthly_avg(year_dict)
			lowest_year = year
	print('''Highest year avg = {high}\nLowest year avg = {low} \
		'''.format(high=highest_year, low=lowest_year))

''' Takes in the yearly_data_dict and returns a dictionary with 
years for keys and monthly averages for values '''
def years_monthly_avg_dict(yearly_data_dict):
	new_dict = {}
	for year in year_list:
		total, year_dict = yearly_trends(yearly_data_dict, year)
		new_dict[f'{year}'] = monthly_avg(year_dict)
	return new_dict


# Returns info specific to the given range
def range_data(data, start_date, end_date):
	month_list = []
	num_list = []
	for month, num in data.items():
		if convert_string(month) >= convert_string(start_date) and convert_string(month) <= convert_string(end_date):
			month_list.append(month)
			num_list.append(num)
	total = sum(num_list)
	new_dict = {month_list[i]: num_list[i] for i in range(len(month_list))}
	return total, start_date, end_date, new_dict
	
# Neatly prints info passed into range_data()
def print_range_data(raw_data, start_date, end_date):
	total, start_date, end_date, new_dict = range_data(raw_data, start_date, end_date)
	return '''{total} times from {start} to {end}
   Avgs for period: monthly = {month} | weekly = {week} | days / time = {days}
           Compare: monthly = {month_diff} | weekly = {week_diff} | days / time = {day_diff} \
   '''.format(total=total, start=start_date, end=end_date, month=monthly_avg(new_dict), week=weekly_avg(new_dict), days=days_per_time(new_dict), month_diff=compare_avg("monthly", new_dict), week_diff=compare_avg("weekly", new_dict), day_diff=compare_avg("daily", new_dict))

month_list_adj = [i[:-5] for i in date_increment(2011)]

# Returns info on frequency by month
def month_trends(data, chosen_month):
	month_list = []
	num_list = []
	for month, num in data.items():
		if chosen_month == month[:-5]:
			month_list.append(month)
			num_list.append(num)
	total = sum(num_list)
	new_dict = {month_list[i]: num_list[i] for i in range(len(month_list))}
	return total, new_dict

def print_month_trends(data, chosen_month):
	total, new_dict = month_trends(data, chosen_month)
	return '''{total} times for {month}
   Avgs for month: monthly = {monthly} | weekly = {week} | days / time = {days}
          Compare: monthly = {month_diff} | weekly = {week_diff} | days / time = {day_diff} \
   '''.format(total=total, month=chosen_month, monthly=monthly_avg(new_dict), week=weekly_avg(new_dict), days=days_per_time(new_dict), month_diff=compare_avg("monthly", new_dict), week_diff=compare_avg("weekly", new_dict), day_diff=compare_avg("daily", new_dict))

def all_months_at_once():
	for month in month_list_adj:
		print(print_month_trends(raw_data, month))

def compare_months():
	test_max = float("-inf")
	test_min = float("inf")
	for chosen_month in month_list_adj:
		total, new_dict = month_trends(raw_data, chosen_month)
		if monthly_avg(new_dict) > test_max:
			test_max = monthly_avg(new_dict)
			highest_month = chosen_month
		if monthly_avg(new_dict) < test_min:
			test_min = monthly_avg(new_dict)
			lowest_month = chosen_month
	print('''Highest month avg = {high}\nLowest month avg = {low} \
		'''.format(high=highest_month, low=lowest_month))

''' Takes raw data and returns a dict with months as keys 
and monthly averages as values '''
def months_monthly_avg_dict(raw_data):
	new_dict = {}
	for month in month_list_adj:
		total, month_dict = month_trends(raw_data, month)
		new_dict[month] = monthly_avg(month_dict)
	return new_dict



season_list = ["Winter", "Spring", "Summer", "Fall"]

''' Takes raw_data and season and returns grand_total and dict
for that season '''
def seasonal_trends(data, season):
	season_dict = {}
	grand_total = 0
	for i in range(3):
		if season == "Winter":
			chosen_month = month_list_adj[(i + 11) % 12]
			total, new_dict = month_trends(raw_data, chosen_month)
			season_dict.update(new_dict)
			grand_total += total
		elif season == "Spring":
			chosen_month = month_list_adj[(i + 2)]
			total, new_dict = month_trends(raw_data, chosen_month)
			season_dict.update(new_dict)
			grand_total += total
		elif season == "Summer":
			chosen_month = month_list_adj[(i + 5)]
			total, new_dict = month_trends(raw_data, chosen_month)
			season_dict.update(new_dict)
			grand_total += total
		elif season == "Fall":
			chosen_month = month_list_adj[(i + 8)]
			total, new_dict = month_trends(raw_data, chosen_month)
			season_dict.update(new_dict)
			grand_total += total
	return grand_total, season_dict
	
def print_seasonal_trends(data, season):
	grand_total, new_dict = seasonal_trends(raw_data, season)
	return '''{total} times during the {season}
   Avgs for season: monthly = {month} | weekly = {week} | days / time = {days}
           Compare: monthly = {month_diff} | weekly = {week_diff} | days / time = {day_diff} \
   '''.format(total=grand_total, season=season.lower(), month=monthly_avg(new_dict), week=weekly_avg(new_dict), days=days_per_time(new_dict), month_diff=compare_avg("monthly", new_dict), week_diff=compare_avg("weekly", new_dict), day_diff=compare_avg("daily", new_dict))

def all_seasons_at_once():
	for season in season_list:
		print(print_seasonal_trends(raw_data, season))

def compare_seasons():
	test_max = float("-inf")
	test_min = float("inf")
	for season in season_list:
		total, new_dict = seasonal_trends(raw_data, season)
		if monthly_avg(new_dict) > test_max:
			test_max = monthly_avg(new_dict)
			highest_season = season
		if monthly_avg(new_dict) < test_min:
			test_min = monthly_avg(new_dict)
			lowest_season = season
	print('''Highest season avg = {high}\nLowest season avg = {low} \
		'''.format(high=highest_season.lower(), low=lowest_season.lower()))

''' Takes raw data and returns a dict with seasons as keys 
and monthly averages as values '''
def seasons_monthly_avg_dict(raw_data):
	new_dict = {}
	for season in season_list:
		grand_total, season_dict = seasonal_trends(raw_data, season)
		new_dict[season] = monthly_avg(season_dict)
	return new_dict


''' Takes in a data dict and returns a dict with
date as keys and current average as values'''
def current_avg(data):
	new_dict = {}
	total = 0
	count = 1
	for date, num in data.items():
		total += num
		avg = total / count
		new_dict[date] = avg
		count += 1
	return new_dict


# Takes a dictionary and labels / titles and makes a bar graph
def make_bar(title, x_label, y_label, data, current, ticks_skip, rotation):
	plt.figure(figsize=(11,7.5))
	plt.bar([i for i in data.keys()], [i for i in data.values()])
	plt.plot([i for i in data.keys()], [monthly_avg(raw_data) for i in data.values()], '--k', label="overall monthly avg (3.9)", linewidth=1)
	if current == "yes":
		plt.plot([i for i in current_avg(data).keys()], [i for i in current_avg(data).values()], 'g', label="current monthly avg", linewidth=2)
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.xticks(list(range(0,len(data),ticks_skip)), rotation=rotation)
	plt.subplots_adjust(bottom=0.2)
	plt.legend()
	plt.savefig(f'/Users/Will/Google Drive File Stream/My Drive/Personal/Weed_Data/{title}.png')
	plt.show()

main()


# Old functions / data that I'm hoarding


'''def make_plot(title, x_label, y_label, data, subplot_num):
	plt.subplot(subplot_num)
	plt.plot([i for i in data.keys()], [i for i in data.values()], linewidth=2)
	plt.plot([i for i in data.keys()], [i for i in data.values()], "b.")
	plt.plot([i for i in data.keys()], [monthly_avg(raw_data) for i in data.values()], '--k', label="overall monthly avg", linewidth=1)
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.xticks(rotation=60)
	plt.gcf().subplots_adjust(bottom=0.3)
	plt.legend()
	#plt.grid(True,color="k")
	#plt.show()
'''
'''
def make_figure():
	#fig = plt.figure(figsize=(6.4, 4.8))
	#			ax1 = fig.add_subplot(312)
	#			ax2 = fig.add_subplot(322)
	#			ax3 = fig.add_subplot(323)
	#			ax = fig.add_subplot(324)
	fig = plt.figure()
	ax1 = plt.subplot2grid((6,2), (0,0), rowspan=3, colspan=2)
	ax2 = plt.subplot2grid((6,2), (4,0), rowspan=1, colspan=2)
	ax3 = plt.subplot2grid((6,2), (5,0), rowspan=1, colspan=1)
	ax4 = plt.subplot2grid((6,2), (5,1), rowspan=1, colspan=1)

	ax1.bar([i for i in raw_data.keys()], [i for i in raw_data.values()])
	ax1.plot([i for i in raw_data.keys()], [monthly_avg(raw_data) for i in raw_data.values()], '--k', label="overall monthly avg", linewidth=1)
	ax1.set_title("All-Time Data")
	ax1.set_xlabel("Months")
	ax1.set_ylabel("Times")


	#make_bar("ax2", "Monthly Averages by Year", "Year", "Monthly Averages", years_monthly_avg_dict(yearly_data_dict), 322)
	#make_bar("ax3", "Monthly Averages by Month", "Month", "Monthly Averages", months_monthly_avg_dict(raw_data), 323)
	#make_bar("ax4", "Monthly Averages by Season", "Season", "Monthly Averages", seasons_monthly_avg_dict(raw_data), 324)

	fig.tight_layout()
	plt.show()
'''

'''def date_increment(start_date, end_date):
	year = start_date.year
	month = start_date.month
	end_year = end_date.year
	end_month = end_date.month
	month_list = []
	while (datetime(end_year, end_month, 1) >= datetime(year, month, 1)) and not ((end_year == year) and (end_month == month)):
		month_list.append(convert_date(datetime(year, month, 1)))
		if month == 12:
			month = 1
			year += 1
		else:
			month +=1
	return month_list'''

'''def seasonal_trends(data, season):
	month_list = []
	num_list = []
	for month, num in data.items():
		if season == "winter" and (month[:-5] == "December" or month[:-5] == "January" or month[:-5] == "February"):
			month_list.append(month)
			num_list.append(num)
		elif season == "spring" and (month[:-5] == "March" or month[:-5] == "April" or month[:-5] == "May"):
			month_list.append(month)
			num_list.append(num)
		elif season == "summer" and (month[:-5] == "June" or month[:-5] == "July" or month[:-5] == "August"):
			month_list.append(month)
			num_list.append(num)
		elif season == "fall" and (month[:-5] == "September" or month[:-5] == "October" or month[:-5] == "November"):
			month_list.append(month)
			num_list.append(num)
	total = sum(num_list)
	new_dict = {month_list[i]: num_list[i] for i in range(len(month_list))}
	return {total} times during the {season}
   Avgs for season: monthly = {month}, weekly = {week}, days / time = {days}
   Compared to overall: monthly = {month_diff}, weekly = {week_diff}, days / time = {day_diff} \
   .format(total=total, season=season, month=monthly_avg(new_dict), week=weekly_avg(new_dict), days=days_per_time(new_dict), month_diff=compare_avg("monthly", new_dict), week_diff=compare_avg("weekly", new_dict), day_diff=compare_avg("daily", new_dict))
'''

'''
data_2010 = {"Jun 2010": 3, "Jul 2010": 2, "Aug 2010": 1, "Sep 2010": 3, "Oct 2010": 9, "Nov 2010": 3, "Dec 2010": 4}
data_2011 = {"Jan 2011": 3, "Feb 2011": 6, "Mar 2011": 3, "Apr 2011": 6, "May 2011": 13, "Jun 2011": 11, "Jul 2011": 3, "Aug 2011": 6, "Sep 2011": 2, "Oct 2011": 4, "Nov 2011": 4, "Dec 2011": 0}
data_2012 = {"Jan 2012": 1, "Feb 2012": 6, "Mar 2012": 0, "Apr 2012": 3, "May 2012": 0, "Jun 2012": 0, "Jul 2012": 0, "Aug 2012": 0, "Sep 2012": 1, "Oct 2012": 5, "Nov 2012": 9, "Dec 2012": 6}
data_2013 = {"Jan 2013": 5, "Feb 2013": 8, "Mar 2013": 11, "Apr 2013": 8, "May 2013": 5, "Jun 2013": 2, "July 2013": 6, "Aug 2013": 1, "Sep 2013": 0, "Oct 2013": 0, "Nov 2013": 3, "Dec 2013": 3}
data_2014 = {"Jan 2014": 3, "Feb 2014": 1, "Mar 2014": 3, "Apr 2014": 1, "May 2014": 2, "Jun 2014": 3, "Jul 2014": 1, "Aug 2014": 3, "Sep 2014": 1, "Oct 2014": 6, "Nov 2014": 2, "Dec 2014": 3}
data_2015 = {"Jan 2015": 3, "Feb 2015": 2, "Mar 2015": 3, "Apr 2015": 3, "May 2015": 5, "Jun 2015": 4, "Jul 2015": 2, "Aug 2015": 2, "Sep 2015": 3, "Oct 2015": 3, "Nov 2015": 5, "Dec 2015": 5}
data_2016 = {"Jan 2016": 4, "Feb 2016": 3, "Mar 2016": 5, "Apr 2016": 7, "May 2016": 4, "Jun 2016": 1, "Jul 2016": 3, "Aug 2016": 2, "Sep 2016": 3, "Oct 2016": 4, "Nov 2016": 5, "Dec 2016": 1}
data_2017 = {"Jan 2017": 0, "Feb 2017": 0, "Mar 2017": 4, "Apr 2017": 6, "May 2017": 2, "Jun 2017": 5, "Jul 2017": 6, "Aug 2017": 4, "Sep 2017": 3, "Oct 2017": 7, "Nov 2017": 6, "Dec 2017": 7}
data_2018 = {"Jan 2018": 4, "Feb 2018": 4, "Mar 2018": 2, "Apr 2018": 5, "May 2018": 5, "Jun 2018": 1, "Jul 2018": 2, "Aug 2018": 5, "Sep 2018": 6, "Oct 2018": 4, "Nov 2018": 7, "Dec 2018": 6}
data_2019 = {"Jan 2019": 8, "Feb 2019": 2, "Mar 2019": 4, "Apr 2019": 4, "May 2019": 3, "Jun 2019": 4, "Jul 2019": 4, "Aug 2019": 4, "Sep 2019": 4, "Oct 2019": 5, "Nov 2019": 10, "Dec 2019": 12}
data_2020 = {"Jan 2020": 11, "Feb 2020": 2}

yearly_data_dict = [zip_list(2010), data_2011, data_2012, data_2013, data_2014, data_2015, data_2016, data_2017, data_2018, data_2019, data_2020]
raw_data = {**data_2010, **data_2011, **data_2012, **data_2013, **data_2014, **data_2015, **data_2016, **data_2017, **data_2018, **data_2019, **data_2020}
'''

