# -*- coding: utf-8 -*-
# from odoo import http


# class Empleados(http.Controller):
#     @http.route('/empleados/empleados', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/empleados/empleados/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('empleados.listing', {
#             'root': '/empleados/empleados',
#             'objects': http.request.env['empleados.empleados'].search([]),
#         })

#     @http.route('/empleados/empleados/objects/<model("empleados.empleados"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('empleados.object', {
#             'object': obj
#         })

