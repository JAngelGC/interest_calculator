"""
    calculator.py

    
"""
import csv
from datetime import datetime, timedelta
from typing import List, Tuple

ESTIMACION_TOTAL: float = 219935.65
TASA_INTERES_ANUAL: float = 0.085
NUM_DIAS_POR_MES: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
DESCUENTO_POR_LIQUIDAR: float = 0.2


def get_interes_mensual(indice_mes, saldo_inicial) -> int:
    """
    Genera el interes dado un mes y una cantidad

    Returns:
        interes_mensual: Interes generado por una cantidad en un mes
    """
    dias_por_anio: int = 365
    interes_mensual: int = round(TASA_INTERES_ANUAL / dias_por_anio * 
                                 NUM_DIAS_POR_MES[indice_mes] * saldo_inicial, 2)
    return interes_mensual


def write_matriz_de_pagos_to_csv(matriz: List[List], filename: str):
    """
    Dada una matriz, la escribe a un archivo csv
    """
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in matriz:
            csv_writer.writerow(row)


def formatear_a_moneda(numero: int) -> str:
    """
    Dado un numero, lo formatea como moneda

    Returns:
        moneda: Numero en el formato deseado
    """
    moneda: int = '$' + '{:20,.2f}'.format(numero).strip()
    return moneda


def generar_test_cases(minimo_numero_de_pagos: int) -> List[object]:
    """
    Genera casos de prueba

    Input:
        minimo_numero_de_pagos: Minimo numero de pagos en los que se puede pagar la deuda
    
    Ouput:
        test_casese: Casos de prueba dado los parametros seleccionados

    Example test_case:
        {"numero_de_pagos": 12, "meses_de_gracia": 0, "meses_para_liquidar": 6}
    """
    maximo_numero_de_pagos: int = 81
    maximo_numero_meses_gracia: int = 3
    meses_para_liquidar: int = 6
    test_cases: List[object] = []

    for i in range(minimo_numero_de_pagos, maximo_numero_de_pagos + 1):
        for j in range(0, maximo_numero_meses_gracia + 1):
            test_cases.append(
                {"numero_de_pagos": i, 
                 "meses_de_gracia": j, 
                 "meses_para_liquidar": meses_para_liquidar}
            )
    
    return test_cases


def calcular_ahorro(numero_de_pagos: int, meses_de_gracia: int, 
                    meses_para_liquidar: int) -> Tuple[float, str, List[List]]:
    """
    Calcula el ahorro que se genera dado los parametros para pagar ESTIMACION_TOTAL

    Notes:
        Num_pago: Número de pago
        Fecha: Fecha de pago
        Saldo_inicial: Dinero que se debe al inicio del mes
        Pago_capital: Dinero mensual que se paga
        Pago_intereses: Dinero mensual que se genera de intereses
        Pago_total: Suma de Pago_capital y Pago_intereses
        Saldo_final:

    Input:
        numero_de_pagos: Mensualidades en las que se desea pagar
        meses_de_gracia: Meses en donde no se hace un pago capital
        meses_para_liquidar: Meses para liquidar la deuda
    
    Returns:
        ahorro_real: Ahorro real que se obtiene por el descuento de liquidar menos
                     los intereses generados
        output: Output generado por el test case
    """

    output = ""
    output += "\n------------------------------------------\n"
    output += "Parameters:\n"
    output += f"- Número de pagos: {numero_de_pagos}\n"
    output += f"- Meses de gracia: {meses_de_gracia}\n"
    output += f"- Meses para liquidar: {meses_para_liquidar}\n\n"

    #           0           1           2               3                  4               5            6               7
    header: List[str] = ["Num Pago", "Fecha", "Saldo inicial", "Pago capital", "Pago intereses", "Pago total", "Saldo final", "Acumulado"]
    matrix: List[List] = [[None] * len(header) for _ in range(numero_de_pagos + meses_de_gracia + 1)]
    matrix[0] = header

    mes_actual: int = 6 + meses_de_gracia
    meses_de_gracia: int = meses_de_gracia
    pago_mensual: int = round(ESTIMACION_TOTAL / (numero_de_pagos), 2)

    # Pagos empiezan en julio de 2023
    fecha: datetime = datetime.strptime("05-jul-2024", "%d-%b-%Y").date()
    saldo_inicial: float = ESTIMACION_TOTAL
    pago_capital: float = pago_mensual
    saldo_final: float = 0
    acumulado: float = 0
    total_interests: float = 0

    numero_total_de_pagos: int = numero_de_pagos + meses_de_gracia
    if meses_para_liquidar > 0:
        numero_total_de_pagos = meses_para_liquidar

    for num_pago in range(1, numero_total_de_pagos + 1):
        pago_intereses: int = get_interes_mensual(mes_actual, saldo_inicial)

        if meses_de_gracia > 0:
            # This is fixed
            pago_capital = 0
            pago_total = 500
            acumulado = round( acumulado + pago_total, 2)
            meses_de_gracia -= 1
        else:
            pago_capital = pago_mensual
            pago_total = round(pago_capital + pago_intereses, 2)
            acumulado = round( acumulado + pago_total, 2)

        saldo_final = round(saldo_inicial - pago_capital , 2)
        
        matrix[num_pago][0] = num_pago
        matrix[num_pago][1] = fecha
        matrix[num_pago][2] = saldo_inicial
        matrix[num_pago][3] = pago_capital
        matrix[num_pago][4] = pago_intereses
        matrix[num_pago][5] = pago_total
        matrix[num_pago][6] = saldo_final
        matrix[num_pago][7] = acumulado

        saldo_inicial = round(saldo_inicial - pago_capital, 2)
        total_interests = round(total_interests + pago_intereses, 2)
        mes_actual = (mes_actual + 1) % len(NUM_DIAS_POR_MES) 
        fecha += timedelta(days=NUM_DIAS_POR_MES[mes_actual])
    
    output += f"Mes para liquidar: {fecha}\n"
    output += f"Total pagado hasta este mes: {formatear_a_moneda(acumulado)}\n"
    output += f"Intereses generados hasta este mes: {formatear_a_moneda(total_interests)}\n\n"

    if saldo_final <= 1:
        output += "Deuda saldada\n"
        return
    
    output += f"Saldo final a liquidar es: {formatear_a_moneda(saldo_final)}\n"
    descuento: float = saldo_final * DESCUENTO_POR_LIQUIDAR
    pago_con_descuento: float = saldo_final - descuento
    output += f"Pago con descuento: {formatear_a_moneda(pago_con_descuento)}\n"
    output += f"Se ahorran: {formatear_a_moneda(descuento)}\n"

    ahorro_real: float = descuento - total_interests
    output += f"Ahorro real (descuento_pago_de_contado - intereses_generados): {formatear_a_moneda(ahorro_real)}\n"

    # Comentar si no se quiere imprimir cada caso de prueba
    print(output)

    return (ahorro_real, output, matrix)
    

def main():
    """
    Primero se obtienen los casos de prueba

    Por cada prueba se obtiene el ahorro real, el output y la matriz de pagos

    Se evaluan todas las opciones y al final se imprime el caso
    de prueba con el mejor ahorro
    """
    minimo_numero_de_pagos: int = 12
    test_cases: List[object] = generar_test_cases(minimo_numero_de_pagos)
    maximo_ahorro: float = 0
    best_output: str = ""
    best_matriz_de_pagos: List[List]
    total_output: str = ""

    for test_case in test_cases:
        current_ahorro: float
        output: str
        current_ahorro, output, matriz = calcular_ahorro(
            numero_de_pagos=test_case["numero_de_pagos"],
            meses_de_gracia=test_case["meses_de_gracia"],
            meses_para_liquidar=test_case["meses_para_liquidar"]
            )
        if current_ahorro > maximo_ahorro:
            maximo_ahorro = current_ahorro
            best_output = output
            best_matriz_de_pagos = matriz
        
        total_output += output


    with open("output.log", "w") as f:
        f.write(total_output)

    write_matriz_de_pagos_to_csv(best_matriz_de_pagos, 'matrix.csv')

    print("\n\n\n\n-----------------------------------------\n")
    print(f"MAXIMO AHORRO: {formatear_a_moneda(maximo_ahorro)} es obtenido por el siguiente test case")
    print(best_output)
    

if __name__ == "__main__":
    main()