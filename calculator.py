"""
    This is a file 
"""

import csv
from datetime import datetime, timedelta
from typing import List

GRACE_MONTHS = 0
NUMBER_OF_PAYMENTS = 12
TOTAL_ESTIMATION = 219935.65
MONTHLY_PAYMENT = round(TOTAL_ESTIMATION / (NUMBER_OF_PAYMENTS), 2)
ANNUAL_INTEREST_RATE = 0.085

MONTHS_TO_SETTLE = 0


DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def get_interests(current_month, saldo_inicial):
    days_per_year = 365
    return round(ANNUAL_INTEREST_RATE / days_per_year * DAYS_PER_MONTH[current_month] * saldo_inicial, 2)

def write_matrix_to_csv(matrix, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in matrix:
            csv_writer.writerow(row)

def print_currency(number):
    return '$' + '{:20,.2f}'.format(number).strip()

def main():
    """
    Num_pago: Número de pago
    Fecha: Fecha de pago
    Saldo_inicial: Dinero que se debe al inicio del mes
    Pago_capital: Dinero mensual que se paga
    Pago_intereses: Dinero mensual que se genera de intereses
    Pago_total: Suma de Pago_capital y Pago_intereses
    Saldo_final:
    """
    #           0           1           2               3                  4               5            6               7
    header = ["Num Pago", "Fecha", "Saldo inicial", "Pago capital", "Pago intereses", "Pago total", "Saldo final", "Acumulado"]
    matrix = [[None] * len(header) for _ in range(NUMBER_OF_PAYMENTS + GRACE_MONTHS + 1)]
    matrix[0] = header

    # Payments start on july
    current_month = 6 + GRACE_MONTHS
    grace_months = GRACE_MONTHS

    fecha = datetime.strptime("05-jul-2024", "%d-%b-%Y").date()
    saldo_inicial = TOTAL_ESTIMATION
    pago_capital = MONTHLY_PAYMENT
    saldo_final = 0
    acumulado = 0
    total_interests = 0

    total_payments = NUMBER_OF_PAYMENTS + GRACE_MONTHS
    if MONTHS_TO_SETTLE > 0:
        total_payments = MONTHS_TO_SETTLE

    for num_pago in range(1, total_payments + 1):
        pago_intereses = get_interests(current_month, saldo_inicial)

        if grace_months > 0:
            # This is fixed
            pago_capital = 0
            pago_total = 500
            acumulado = round( acumulado + pago_total, 2)
            grace_months -= 1
        else:
            pago_capital = MONTHLY_PAYMENT
            pago_total = pago_capital + pago_intereses
            acumulado = round( acumulado + pago_total, 2)

        matrix[num_pago][0] = num_pago
        matrix[num_pago][1] = fecha
        matrix[num_pago][2] = saldo_inicial
        matrix[num_pago][3] = pago_capital
        matrix[num_pago][4] = pago_intereses
        
        pago_total = round(pago_capital + pago_intereses, 2)
        matrix[num_pago][5] = pago_total

        saldo_final = round(saldo_inicial - pago_capital , 2)
        matrix[num_pago][6] = saldo_final
        matrix[num_pago][7] = acumulado

        saldo_inicial = round(saldo_inicial - pago_capital, 2)
        total_interests = round(total_interests + pago_intereses, 2)
        current_month = (current_month + 1) % len(DAYS_PER_MONTH) 
        fecha += timedelta(days=DAYS_PER_MONTH[current_month])
    


    filename = 'matrix.csv'
    write_matrix_to_csv(matrix, filename)


    print(f"Total pagado: {print_currency(acumulado)}")
    print(f"Intereses generados: {print_currency(total_interests)}")

    if saldo_final <= 1:
        print("Deuda saldada")
        return
    print("------------------")
    
    print(f"Saldo final a liquidar es: {print_currency(saldo_final)}")
    descuento = saldo_final * 0.2
    pago_con_descuento = saldo_final - descuento
    print(f"Pago con descuento: {print_currency(pago_con_descuento)}")
    print(f"Se ahorran: {print_currency(descuento)}")
    













if __name__ == "__main__":
    main()
