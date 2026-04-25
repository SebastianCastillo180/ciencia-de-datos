
#librerias 
import pyodbc 

#Se hace la conexión
conexionString ='DRIVER={SQL Server};SERVER=192.168.0.139\BODEGA;DATABASE=DataStage;UID=odbc;PWD=Odbc.2019'
conexion = pyodbc.connect(conexionString)

#se creaa variable 
crear = ("CREATE TABLE dbo.t200_mm_terceros(f200_id_cia smallint NULL, f200_rowid int NULL, f200_id char(15) NULL, f200_nit varchar(25) NULL,	f200_dv_nit char(3) NULL, f200_id_tipo_ident char(1) NULL,	f200_ind_tipo_tercero smallint NULL, f200_razon_social varchar(100) NULL, 	f200_apellido1 varchar(30) NULL) ")
query2 = ("INSERT INTO DataStage.dbo.t200_mm_terceros (f200_id_cia, f200_rowid ,f200_id ,f200_nit ,f200_dv_nit ,f200_id_tipo_ident ,f200_ind_tipo_tercero ,f200_razon_social ,f200_apellido1 ) SELECT f200_id_cia, f200_rowid ,f200_id ,f200_nit ,f200_dv_nit ,f200_id_tipo_ident ,f200_ind_tipo_tercero ,f200_razon_social ,f200_apellido1   FROM SIESA.dbo.t200_mm_terceros")

#se ejecuta instruccion 
conexion.execute(crear)
conexion.execute(query2)
conexion.commit()

#se sierra la conexión
conexion.close()
