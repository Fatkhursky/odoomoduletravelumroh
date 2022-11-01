from odoo import api, fields, models
 
class TravelXlsx(models.AbstractModel):
    _name = 'report.travel_umroh.report_travel'
    _description = 'Report Travel Umroh'
    _inherit = 'report.report_xlsx.abstract'
 
    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet('Travel %s' % obj.name)
        text_top_style = workbook.add_format({'font_size': 12, 'bold': True ,'font_color' : 'black','font' : 'Abyssinica SIL' ,'bg_color': '#ffb011', 'valign': 'vcenter', 'align': 'center', 'left': 1, 'bottom':1, 'right':1, 'top':1 , 'text_wrap': True})
        text_header_style = workbook.add_format({'font_size': 11, 'bold': True ,'font_color' : 'white', 'font' : 'Abyssinica SIL' , 'bg_color': '#1932b0','left': 1, 'bottom':1, 'right':1, 'top':1, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        text_style = workbook.add_format({'font_size': 12, 'valign': 'vcenter', 'text_wrap': True,'font' : 'Abyssinica SIL' , 'align': 'center','left': 1, 'bottom':1, 'right':1, 'top':1})
        number_style = workbook.add_format({'num_format': '#,##0', 'font_size': 12, 'align': 'right','font' : 'Abyssinica SIL' , 'valign': 'vcenter', 'text_wrap': True, 'left': 1, 'bottom':1, 'right':1, 'top':1})
        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mmmm-yyyy', 'align': 'center','font' : 'Abyssinica SIL' , 'left': 1, 'bottom':1, 'right':1, 'top':1})
        id_style = workbook.add_format({'font_size': 12, 'bold': True ,'font_color' : 'black', 'bg_color': '#ffb011', 'font' : 'Abyssinica SIL' ,'valign': 'vcenter', 'align': 'center', 'left': 1, 'bottom':1, 'right':1, 'top':1 , 'text_wrap': True})

        # sheet.merge_range(0, 0, 0, 1, "Reference", text_top_style)
        #sheet.merge_range('A1:C1', "Manifest", text_top_style)
        sheet.merge_range('C2:D2', "Manifest", text_top_style)
        sheet.merge_range('E2:G2', "", text_top_style)
        sheet.write('E2', obj.name, id_style)

        row = 5
        sheet.freeze_panes(6, 18)
        sheet.set_column(0, 0, 5)
        sheet.set_column(3, 9, 17)
        sheet.set_column(12, 17, 15)
        header = ['No', 'Title', 'Gender', 'Full Name', 'Tempat Lahir','Tanggal Lahir', 'No. Passport', 'Passport Issued','Passport Expired','Imigrasi', 'Mahrom', 'Usia', 'NIK', 'Order', 'Room Type', 'Room Leader', 'No. Room', 'Alamat']
        header2 = ['No', 'Airline', 'Departure Date', 'Departure City', 'Arrival City']
        sheet.write_row(row, 0, header, text_header_style)
        sheet.write_row((row + len(obj.manifest_line) + 4), 2, header2, text_header_style)

        # Data tabel 1 
        no_list = []
        title = []
        gender = []
        full_name = []
        tempat_lahir = []
        tanggal_lahir = []
        no_passport = []
        passport_issued = []
        passport_expired = []
        imigrasi = []
        mahrom = []
        usia = []
        nik = []
        order = []
        room_type = []
        room_leader = []
        no_room = []
        alamat = []

        #Data tabel 2
        num = []
        airline = []
        departure_date = []
        departure_city = []
        arrival_city = []

 
        no = 1
        for x in obj.manifest_line:
            no_list.append(no)
            title.append(x.title)
            gender.append(x.jenis_kelamin.capitalize())
            full_name.append(x.nama_passport)
            tempat_lahir.append(x.tempat_lahir or '')
            tanggal_lahir.append(x.tanggal_lahir or '')
            no_passport.append(x.no_passport or '')
            passport_issued.append(x.tanggal_berlaku or '')
            passport_expired.append(x.tanggal_expired or '')
            imigrasi.append(x.imigrasi or '')
            mahrom.append(x.mahrom or '')
            usia.append(x.umur or '')
            nik.append(x.no_ktp or '')
            order.append(x.order or '')
            room_type.append(x.tipe_kamar or '')
            room_leader.append('-')
            no_room.append('-')
            alamat.append(x.alamat)
           
            no+=1

        no2 = 1
        for y in obj.airline_line:
            num.append(no2)
            airline.append(y.airline_name_id.name)
            departure_date.append(y.tanggal_berangkat)
            departure_city.append(y.kota_asal)
            arrival_city.append(y.kota_tujuan)

      
           
            no2+=1
 
        row += 1
        sheet.write_column(row, 0, no_list, text_style)
        sheet.write_column(row, 1, title, text_style)
        sheet.write_column(row, 2, gender, text_style)
        sheet.write_column(row, 3, full_name, text_style)
        sheet.write_column(row, 4, tempat_lahir, text_style)
        sheet.write_column(row, 5, tanggal_lahir, date_style)
        sheet.write_column(row, 6, no_passport, text_style)
        sheet.write_column(row, 7, passport_issued, date_style)
        sheet.write_column(row, 8, passport_expired, date_style)
        sheet.write_column(row, 9, imigrasi, text_style)
        sheet.write_column(row, 10, mahrom, text_style)
        sheet.write_column(row, 11, usia, text_style)
        sheet.write_column(row, 12, nik, number_style)
        sheet.write_column(row, 13, order, text_style)
        sheet.write_column(row, 14, room_type, text_style)
        sheet.write_column(row, 15, room_leader, text_style)
        sheet.write_column(row, 16, no_room, text_style)
        sheet.write_column(row, 17, alamat, text_style)
 
        row = row + len(obj.manifest_line) + 4
        sheet.write_column(row, 2, num, text_style)
        sheet.write_column(row, 3, airline, text_style)
        sheet.write_column(row, 4, departure_date, date_style)
        sheet.write_column(row, 5, departure_city, text_style)
        sheet.write_column(row, 6, arrival_city, text_style)