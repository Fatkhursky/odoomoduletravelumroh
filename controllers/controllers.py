# -*- coding: utf-8 -*-
# from odoo import http


# class AaTravelUmroh(http.Controller):
#     @http.route('/aa_travel_umroh/aa_travel_umroh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aa_travel_umroh/aa_travel_umroh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aa_travel_umroh.listing', {
#             'root': '/aa_travel_umroh/aa_travel_umroh',
#             'objects': http.request.env['aa_travel_umroh.aa_travel_umroh'].search([]),
#         })

#     @http.route('/aa_travel_umroh/aa_travel_umroh/objects/<model("aa_travel_umroh.aa_travel_umroh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aa_travel_umroh.object', {
#             'object': obj
#         })
