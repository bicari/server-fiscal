import pyodbc
import asyncio
from socketio import AsyncServer
from datetime import datetime
import pathlib
import os
import zipfile
from utils.read_ini import loadLastAuto, updateAuto

async def buscarVentas(server: AsyncServer, time_to_stop: float):
    while True:
        autoIni=loadLastAuto()
        with pyodbc.connect("DSN=A2GKC") as conn:
            with conn.cursor() as cursor:
                lastAuto=cursor.execute(f"""SELECT MAX (FTI_AUTOINCREMENT)
                          FROM SOPERACIONINV
                          WHERE FTI_STATUS = 1 AND FTI_FECHAEMISION = '{str(datetime.date(datetime.now()))}' 
                          """).fetchval()
            
            print(lastAuto)
            if lastAuto > int(autoIni):
                with conn.cursor() as cursor:
                    cursor.execute(f"""SELECT * INTO "{str(pathlib.Path().absolute())+ "/tmp/Ventas"}" FROM SOPERACIONINV 
                                        WHERE FTI_FECHAEMISION = '{str(datetime.date(datetime.now()))}' AND
                                        FTI_AUTOINCREMENT > {autoIni} AND FTI_AUTOINCREMENT <= {lastAuto} """)
                    #cursor.execute(f"""SELECT * INTO "{str(pathlib.Path().absolute()) + "/tmp/Ventas" }"  FROM SOPERACIONINV WHERE FTI_AUTOINCREMENT = {lastAuto}""")
                    #cursor.execute(f"""SELECT * INTO "{str(pathlib.Path().absolute()) + "/tmp/Detalle" }"  FROM SDETALLEVENTA WHERE FDI_OPERACION_AUTOINCREMENT = {lastAuto}""")
                cursor.close()
                await compactarTablas()
                #await server.emit('enviar_facturas', data={'factura': lastAuto})    
        await asyncio.sleep(time_to_stop)


async def compactarTablas() :
    try:
        zip_File = zipfile.ZipFile('ventasF.zip', 'w')
        result = next(os.walk(f'{str((pathlib.Path().absolute()))}/tmp'))[2]
        print(result)
        for file in result:
            if file[:-4] in ['Ventas', 'Detalle'] and file.endswith(('.idx', '.dat', '.blb')):
                zip_File.write(filename='{path}{file_name}'.format(path=f'tmp\\', file_name=file), arcname=file, compress_type=zipfile.ZIP_DEFLATED)

    except Exception as e:
        print(e)


        
