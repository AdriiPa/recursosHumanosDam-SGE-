from odoo import models, fields, api
from datetime import date
import logging

logger=logging.getLogger(__name__)

class empleados(models.Model):
    _name = 'empleados.empleados'
    _description = 'Empleados'

    nombre=fields.Char(string="Nombre: ",required=True)
    apellido1=fields.Char(string="Apellido1: ",required=True)
    apellido2=fields.Char(string="Apellido2: ",required=True)
    nombre_completo=fields.Char(compute="get_nombre_completo",string="Nombre Completo: ")
    dni=fields.Char(string="DNI: ",required=True)
    edad=fields.Integer(compute="get_edad_fecha", string="Edad: ")
    fechaNacimiento=fields.Date(string="Fecha de nacimiento: ",required=True)
    sueldoBrutoAnual=fields.Float(string="Sueldo Bruto Anual: ",required=True)
    fechaInicioContrato=fields.Date(string="Fecha de inicio de contrato: ",required=True)
    fechaFinContrato=fields.Date(string="Fecha de inicio de contrato: ",)
    estado=fields.Char(compute="get_estado",string="Estado: ")
    codigoEmpleado=fields.Char(compute="get_codigo_empleado",string="Codido de empleado :")
    imagen=fields.Binary("Foto del empleado: ",attachment=True)


    @api.depends('nombre','apellido1','apellido2')
    def get_nombre_completo(self):
        for emp in self:
            if emp.nombre and emp.apellido1 and emp.apellido2:
                emp.nombre_completo = f"{emp.nombre} {emp.apellido1} {emp.apellido2}"
            else:
                emp.nombre_completo="Sin definir"
            
            logger.info(f"Nombre completo calculado :{emp.nombre_completo}")

    
    @api.depends('fechaNacimiento')
    def get_edad_fecha(self):
        for emp in self:
            if emp.fechaNacimiento:
                hoy = date.today()
                emp.edad = hoy.year - emp.fechaNacimiento.year - (
                    (hoy.month, hoy.day) < (emp.fechaNacimiento.month, emp.fechaNacimiento.day))
            else:
                emp.edad = 0
            
            logger.info(f"Edad calculada para {emp.nombre}: {emp.edad}")
    
    @api.depends('fechaFinContrato')
    def get_estado(self):
        for emp in self:
            if emp.fechaFinContrato:
                emp.estado="BAJA"
            else:
                emp.estado="ACTIVO"
            
            logger.info(f"Estado calculado para {emp.nombre}: {emp.estado}")
    
    @api.depends('dni','fechaInicioContrato')
    def get_codigo_empleado(self):
        for emp in self:
            if emp.dni and emp.fechaInicioContrato:
                ult5Cifras=emp.dni[-5:]
                fecha_inicioSTR=emp.fechaInicioContrato.strftime('%d%m%y')
                emp.codigoEmpleado=f"COD_{ult5Cifras}_{fecha_inicioSTR}"
            else:
                emp.codigoEmpleado="Sin definir"
            
            logger.info(f"Código de empleado calculado para {emp.nombre}: {emp.codigoEmpleado}")



class empresas(models.Model):
    _name="empleados.empresas"
    _description="Empresas"

    cifEmpresa=fields.Char(string="CIF Empresa:", required=True)
    nombreEmpresa=fields.Char(string="Nombre de la empresa:", required=True)
    nombreCompletoEmpresa=fields.Char(string="Nombre Completo: ",compute="get_nombreCompletoEmpresa")

    EMPRESAS_DICT = {
    'Amazon': 'AMAZON S.A.',
    'Google': 'GOOGLE INC.',
    'Facebook': 'META PLATFORMS INC.',
    'Microsoft': 'MICROSOFT CORPORATION',
    'Apple': 'APPLE INC.',
    'Tesla': 'TESLA MOTORS INC.',
    'Netflix': 'NETFLIX INC.',
    'IBM': 'INTERNATIONAL BUSINESS MACHINES CORP.',
    'Oracle': 'ORACLE CORPORATION',
    'Intel': 'INTEL CORPORATION',
    'Samsung': 'SAMSUNG ELECTRONICS CO., LTD.',
    'Sony': 'SONY CORPORATION',
    'LG': 'LG ELECTRONICS INC.',
    'Huawei': 'HUAWEI TECHNOLOGIES CO., LTD.',
    'Xiaomi': 'XIAOMI CORPORATION',
    }

    @api.depends('nombreEmpresa')
    def get_nombreCompletoEmpresa(self):
        for emp in self:
            nombreEmpresaDic = emp.nombreEmpresa

            # Asegúrate de que nombreEmpresaDic sea una cadena
            if not isinstance(nombreEmpresaDic, str):
                emp.nombreCompletoEmpresa = "Nombre Inválido"  # O un valor predeterminado
                continue

            if nombreEmpresaDic in self.EMPRESAS_DICT:
                emp.nombreCompletoEmpresa = self.EMPRESAS_DICT[nombreEmpresaDic]
            else:
                emp.nombreCompletoEmpresa = nombreEmpresaDic.upper()

            logger.info(f"Nombre calculado para {emp.nombreEmpresa}: {emp.nombreCompletoEmpresa}")


class calculadoraSueldo(models.Model):
    _name="empleados.calculadora_sueldo"
    _description="Calculadora para calcular Sueldo Neto Mensual"
    nombreConsultor=fields.Char(string="Nombre: ")
    sueldoBruto=fields.Float(string="Sueldo Bruto Anual: ",required=True)
    numeroPagas=fields.Selection(selection=[('12','12 Pagas'),('14','14 Pagas')], string="Numero de pagas: ",required=True,default="12")
    mensualidadBruta=fields.Float(compute="get_mensualidadBruta",string="Mensualidad Bruta: ")
    mensualidadNeta=fields.Float(compute="get_sueldoNetoMensual", string="Sueldo Neto Mensual: ")
    irpfPagadoAnual=fields.Float(compute="get_irpfAnual", string= "IRPF pagado anualmente: ")
    irpfPagadoMes=fields.Float(compute="get_irpfMensual",string="IRPF pagado mensualmente: ")

    @api.depends('sueldoBruto','numeroPagas')
    def get_mensualidadBruta(self):
        for sld in self:

            pagas=int(sld.numeroPagas)
            sld.mensualidadBruta=sld.sueldoBruto/pagas

            logger.info(f"Mensualidad Bruta calculada: {sld.mensualidadBruta} para {sld.nombreConsultor}")
            
            
    
    def get_tramoIrpf(self,sueldoBruto):
        if sueldoBruto <= 12450:
            return 0.19
        elif sueldoBruto > 12450 and sueldoBruto <= 20200:
            return 0.24
        elif sueldoBruto > 20200 and sueldoBruto <= 35200:
            return 0.30
        elif sueldoBruto > 35200 and sueldoBruto <= 60000:
            return 0.37
        else:
            return 0.45
    
    @api.depends('sueldoBruto')
    def get_irpfAnual(self):
        for sld in self:

            porcentajeIrpf=self.get_tramoIrpf(sld.sueldoBruto)
            sld.irpfPagadoAnual=self.sueldoBruto * porcentajeIrpf

            logger.info(f"IRPF Anual calculado: {sld.irpfPagadoAnual} para {sld.nombreConsultor}")
            
    
    @api.depends('irpfPagadoAnual','numeroPagas')
    def get_irpfMensual(self):
        for sld in self:

            pagas=int(sld.numeroPagas)
            sld.irpfPagadoMes=sld.irpfPagadoAnual / pagas

            logger.info(f"IRPF Mensual calculado: {sld.irpfPagadoMes} para {sld.nombreConsultor}")
    
    @api.depends('sueldoBruto','irpfPagadoMes')
    def get_sueldoNetoMensual(self):
        for sld in self:
            sld.mensualidadNeta=sld.mensualidadBruta - sld.irpfPagadoMes

            logger.info(f"Sueldo Neto Mensual calculado: {sld.mensualidadNeta} para {sld.nombreConsultor}")







