from email.policy import default
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta    

class TravelPackage(models.Model):
    _name = 'travel.package'
    _description = 'Paket Perjalanan'

    @api.depends('hpp_line.sub_total')
    def _amount_total(self):
        for o in self:
            o.update({
                'amount_total': sum([l.sub_total for l in o.hpp_line])
            })
    
    @api.depends('manifest_line', 'quota')
    def compute_quota(self):
        for i in self:
            i.remaining_quota = i.quota - len(i.manifest_line)
            i.quota_progress = 100 *  len(i.manifest_line) / i.quota 
           
                 
            #data = len(self.env['manifest.line'].search_read([], ['nama_passport']))
            # if i.quota:
            #     i.remaining_quota = i.quota - data
            #     i.quota_progress = 100 *  data / i.quota  

    hide_action_buttons = fields.Boolean('Hide Action Buttons', compute='_compute_hide_action_buttons')
    


    name = fields.Char('Reference', default='-', readonly=True)
    manifest_line = fields.One2many('manifest.line', 'package_manifest_id', string='Manifest Lines')
    hpp_line = fields.One2many('hpp.line', 'package_hpp_id', string='Hpp Lines')
    hotel_line = fields.One2many('hotel.line', 'package_hotel_id', string='Hotel Lines')
    airline_line = fields.One2many('airline.line', 'package_airline_id', string='Airline Lines')
    schedule_line = fields.One2many('schedule.line', 'package_schedule_id', string='Schedule Lines')

    # order_id = fields.Many2one('sale.order',  string='Order Id',domain=[('state', '=', 'sale')]) 
    product_package_id = fields.Many2one('product.product', required=True, readonly=True, states={'draft' : [('readonly', False)]})
    amount_total = fields.Monetary('Total Cost', store=True, compute='_amount_total')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    departure_date = fields.Date('Tanggal Berangkat', required=True, default=fields.Date.context_today, readonly=True, states={'draft' : [('readonly', False)]})
    return_date = fields.Date('Tanggal Kembali', required=True, readonly=True, states={'draft' : [('readonly', False)]})
    product_sale_id = fields.Many2one('product.product', string='Sale', required=True, readonly=True, states={'draft' : [('readonly', False)]})
    quota = fields.Integer('Quota' ,default=20 ,readonly=True, states={'draft' : [('readonly', False)]})
    remaining_quota = fields.Integer('Remaining Quota', compute='compute_quota')
    quota_progress = fields.Float('Quota Progress',compute='compute_quota' )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
    ], string='Status', readonly=True, copy=False, default='draft')
   
    @api.model
    def create(self, vals):
        #sale_name = self.env['product.product'].browse(vals.get('sale_id')).name HARUS GETNAME
        vals['name'] = self.env['ir.sequence'].next_by_code('travel.package') 
        return super(TravelPackage, self).create(vals)


    @api.onchange('product_package_id')
    def _onchange_package_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for res in rec.product_package_id.bom_ids:       
                for i in res.bom_line_ids:    
                    val = {
                    'product_id' : i.product_id,
                    'product_qty' : i.product_qty,
                    'product_uom_id': i.product_uom_id.name,
                    'unit_price' : i.product_id.standard_price,
                    'sub_total' : i.product_qty * i.product_id.standard_price,
                    }
                    lines.append((0,0,val))
            rec.hpp_line = lines

    def package_draft(self):
        for o in self:
            return o.write({'state': 'draft'})

    def package_open(self):
        for o in self:
            return o.write({'state': 'confirm'})
 
    def package_done(self):
        for o in self:
            return o.write({'state': 'done'})

    def update_jamaah(self):
        #self.order_id = self.env['sale.order'].search([  ('state', '=', 'sale'), ('paket_id', '=', self.name)])
        b = self.env['sale.order'].search([  ('state', 'in', ('sale', 'done')), ('paket_id', '=', self.id) ])
        # print('--->id package', self.id)
        # print('--->id sale order', b.passport_line)
        for rec in self:
            lines = [(5, 0, 0)]
            for i in b.passport_line:
                val = {
                    'title' : i.title,
                    'nama_passport' : i.nama_passport,
                    'jenis_kelamin' : i.jenis_kelamin,
                    'no_ktp' : i.no_ktp,
                    'no_passport' : i.no_passport,
                    'tanggal_lahir' : i.tanggal_lahir,
                    'tempat_lahir' : i.tempat_lahir,
                    'tanggal_berlaku' : i.tanggal_berlaku,
                    'tanggal_expired' : i.tanggal_expired,
                    'imigrasi' : i.imigrasi,
                    'tipe_kamar' : i.tipe_kamar,
                    'mahrom' : i.mahrom_id.name,
                    'agent' : i.agent_id.name,
                    'umur': i.umur,
                    'order': i.sale_id.name,
                    'alamat': i.alamat
                    }
                lines.append((0,0,val))
            rec.manifest_line = lines

    def print_manifest(self):
        return self.env.ref('ab_travel_umroh.report_travel_umroh_action').report_action(self)  


class HotelLine(models.Model):
    _name = 'hotel.line'
    _description = 'Hotel Line'
  
    city = fields.Char('Kota' ,related='hotel_id.city')
    hotel_id = fields.Many2one('res.partner', string='Nama Hotel')
    check_in_hotel = fields.Date('Check In Hotel')
    check_out_hotel = fields.Date('Check Out Hotel')
    package_hotel_id = fields.Many2one('travel.package', string='Package Reference', required=True, ondelete='cascade')

class AirlineLine(models.Model):
    _name = 'airline.line'
    _description = 'Airline Line'

    package_airline_id = fields.Many2one('travel.package', string='Package Reference', required=True, ondelete='cascade')
    airline_name_id = fields.Many2one('res.partner', string='Nama Airline')
    tanggal_berangkat = fields.Date('Tanggal Berangkat')
    kota_asal = fields.Char('Kota Asal')
    kota_tujuan = fields.Char('Kota Tujuan')


class ScheduleLine(models.Model):
    _name = 'schedule.line'
    _description = 'Schedule Line'

    package_schedule_id = fields.Many2one('travel.package', string='Package Reference', required=True, ondelete='cascade')
    tanggal_kegiatan = fields.Date('Tanggal Kegiatan')
    nama_kegiatan = fields.Char('Nama Kegiatan')


class ManifestLine(models.Model):
    _name = 'manifest.line'
    _description = 'Manifest Line'
  
    no_passport = fields.Char('No. Passport')  
    imigrasi = fields.Char('Imigrasi')  
    tanggal_lahir = fields.Date('Tanggal Lahir')
    tanggal_expired = fields.Date('Tanggal Expired')
    tanggal_berlaku = fields.Date('Tanggal Berlaku')
    no_ktp = fields.Char('no_ktp')
    tempat_lahir = fields.Char('tempat_lahir')  
    package_manifest_id = fields.Many2one('travel.package', string='Package Manifest Reference', required=True, ondelete='cascade')
    title = fields.Char('Title')
    nama_passport = fields.Char('nama_passport')
    jenis_kelamin = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan'),
    ], string='jenis_kelamin')
    tipe_kamar = fields.Selection(string='Tipe Kamar', selection=[('double', 'Double'), ('triple', 'Triple'), ('quad', 'Quad')])
    umur = fields.Integer('Umur')
    order = fields.Char('Order')
    alamat = fields.Char('Alamat')
    mahrom = fields.Char('Mahrom')
    agent = fields.Char('Agent')



class HppLine(models.Model):
    _name = 'hpp.line'
    _description = 'Hpp Line'


    @api.depends('product_qty')
    def _compute_total(self):
        for o in self:
            o.update({
                'sub_total': o.unit_price * o.product_qty       
            })
 
    
    product_id = fields.Many2one('product.product', required=True)     
    product_qty = fields.Float('product_qty,'  )  
    product_uom_id = fields.Char('product_uom_id' )     
    unit_price = fields.Float('unit_price' )     
    sub_total = fields.Float('sub_total', compute='_compute_total')
    package_hpp_id = fields.Many2one('travel.package', string='Package Reference', required=True, ondelete='cascade')
    product_price = fields.Float('product_price')
    


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_description = fields.Char(string='Partner Description')
    travel_type = fields.Selection(string='Travel', selection=[('hotel', 'Hotel'), ('airline', 'Airline')])
    is_hotel= fields.Boolean('Hotel', default=False)
    is_airline= fields.Boolean('Airline', default=False)
   
    # Additional Form Field
    no_ktp = fields.Char('no_ktp')
    nama_ayah = fields.Char('nama_ayah') 
    pekerjaan_ayah = fields.Char('pekerjaan_ayah')
    tempat_lahir = fields.Char('tempat_lahir')  
    nama_ibu = fields.Char('nama_ibu') 
    pekerjaan_ibu = fields.Char('pekerjaan_ibu')
    no_passport = fields.Char('no_passport')  
    imigrasi = fields.Char('imigrasi') 
    nama_passport = fields.Char('nama_passport')
    status_pernikahan = fields.Selection([
        ('single', 'Belum Menikah'),
        ('married', 'Menikah'),
        ('divorced', 'Cerai'),
    ], string='status_pernikahan', help='Status Pernikahan')
    pendidikan_terakhir = fields.Selection([
        ('primary school', 'SD'),
        ('junior high school', 'SMP'),
        ('senior high school', 'SMA'),
        ('diploma', 'Diploma'),
        ('bachelor', 'S1'),
        ('master', 'S2'),
        ('doctor', 'S3'),
    ], string='pendidikan_terakhir', help='Pendidikan Terakhir')
    jenis_kelamin = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan'),
    ], string='jenis_kelamin')
    golongan_darah = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O'),
    ], string='golongan_darah')
    ukuran_baju = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
    ], string='ukuran_baju')
    tanggal_lahir = fields.Date('tanggal_lahir')
    tanggal_berlaku = fields.Date('tanggal_berlaku')
    tanggal_expired = fields.Date('tanggal_expired')
    scan_passport = fields.Binary('scan_passport')
    scan_ktp = fields.Binary('scan_ktp')
    scan_buku_nikah = fields.Binary('scan_buku_nikah')
    scan_kartu_keluarga = fields.Binary('scan_kartu_keluarga')



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    passport_line = fields.One2many('passport.line', 'sale_id', string='Passport Line')
    paket_id = fields.Many2one('travel.package', string='Paket Perjalanan', domain=[('state', '=', 'confirm')])

    @api.onchange('paket_id')
    def _onchange_paket_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            # print("-------------------->>>", rec.paket_id.sale_id.product_tmpl_id.standard_price)
            for res in rec.paket_id.product_sale_id:       
                val = {
                'product_id' : res,
                'name' : res.name,
                'product_uom': res.uom_id,
                # 'product_uom_qty' : self.product_uom_qty, product.product
                'price_unit' : res.product_tmpl_id.standard_price,
                'tax_id': res.taxes_id
        
                }
                lines.append((0,0,val))
                # print("-------------------->", res.product_tmpl_id.standard_price)
            rec.order_line = lines
    
class PassportLine(models.Model):
    _name = 'passport.line'
    _description = 'Passport Line'

    sale_id = fields.Many2one('sale.order', string='Order Reference',  ondelete='cascade')
    
    @api.depends('tanggal_lahir')
    def _get_age(self):
        for r in self:
            if r.tanggal_lahir and r.tanggal_lahir <= fields.Date.today():
                r.umur = relativedelta(
                fields.Date.from_string(fields.Date.today()),
                fields.Date.from_string(r.tanggal_lahir)).years 
            else:
                r.umur = 0
    
    title = fields.Char('Title', related='jamaah_id.title.name')
    nama_passport = fields.Char('Nama Passport', related='jamaah_id.nama_passport')
    jenis_kelamin = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan'),
    ], string='Jenis Kelamin', related='jamaah_id.jenis_kelamin')
    no_ktp = fields.Char('No. KTP', related='jamaah_id.no_ktp')
    no_passport = fields.Char('No. Passport', related='jamaah_id.no_passport')  
    tanggal_lahir = fields.Date('Tanggal Lahir', related='jamaah_id.tanggal_lahir')
    tempat_lahir = fields.Char('Tempat Lahir', related='jamaah_id.tempat_lahir')  
    tanggal_berlaku = fields.Date('Tanggal Berlaku', related='jamaah_id.tanggal_berlaku')
    tanggal_expired = fields.Date('Tanggal Expired', related='jamaah_id.tanggal_expired')
    imigrasi = fields.Char('Imigrasi', related='jamaah_id.imigrasi') 
    tipe_kamar = fields.Selection(string='Tipe Kamar',
        selection=[('double', 'Double'), ('triple', 'Triple'), ('quad', 'Quad')], default="double")
    umur = fields.Integer('Umur', store=True, compute='_get_age')
    mahrom_id = fields.Many2one('res.partner', 'Mahrom')
    agent_id = fields.Many2one('res.users', string='My User',default=lambda self: self.env.user)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    #Field Form Manifest Line
    jamaah_id = fields.Many2one('res.partner', string='Nama Jamaah')
    notes = fields.Char('Notes')
    scan_passport = fields.Binary('Scan Passport', related='jamaah_id.scan_passport')
    scan_ktp = fields.Binary('Scan KTP', related='jamaah_id.scan_ktp')
    scan_buku_nikah = fields.Binary('Scan Buku Nikah', related='jamaah_id.scan_buku_nikah')
    scan_kartu_keluarga = fields.Binary('Scan Kartu Keluarga', related='jamaah_id.scan_kartu_keluarga')
    alamat = fields.Char('Alamat', related='jamaah_id.city')

class StockPicking(models.Model):
    _inherit = ['stock.picking']

    def print_delivery(self):
        return self.env.ref('ab_travel_umroh.report_pdf_travel_umroh_action').report_action(self)

class AccountMove(models.Model):
    _inherit = ['account.move']

    def print_delivery(self):
        return self.env.ref('ab_travel_umroh.report_pdf_travel_invoice_action').report_action(self)
  
