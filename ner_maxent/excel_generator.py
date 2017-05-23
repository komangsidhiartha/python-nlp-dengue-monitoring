import dbmodel as db
import pandas as pd

years = ['2017', '2016', '2015']
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

xls_path = '../Database/excel/data.xls'

def generate():
	dbmodel = db.DBModel()
	writer = pd.ExcelWriter(xls_path)

	for year in years:
		for month in months:
			fwc_db = "%s_fwc"%year
			datas = dbmodel.top_location_of_month(fwc_db,month)

			df = pd.DataFrame(list(datas))
			if not df.empty:
				df.rename(index=str, columns={"NUM": "Jumlah Kejadian", "_id": "Lokasi"})[['Lokasi','Jumlah Kejadian']].to_excel(writer,'%s - %s' % (year, month))

	writer.save()