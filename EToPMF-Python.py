"""
    Estimativa de evapotranspiração de referência pelo método de Penman-Monteith-FAO (EToPMF) com Python
    ====================================================================================================

    @authors    Isak Paulo de Andrade Ruas <isakruas@gmail.com>
                Sibele Pinheiro da Silva <sibelepinheirosilva@gmail.com>

    @license    Este código é disponibilizado sobre a Licença Pública Geral (GNU) V3.0
                Mais detalhes em: https://github.com/isakruas/EToPMF-Python/blob/master/LICENSE

    @link       Homepage:     https://isakruas.blogspot.com/2020/11/EToPMF-Python.html
                GitHub Repo:  https://github.com/isakruas/EToPMF-Python/
                README:       https://github.com/isakruas/EToPMF-Python/blob/master/README.md

    @version    1.0.00
"""

import datetime
import math

print('')
print('Estimativa de evapotranspiração de referência pelo método de Penman-Monteith-FAO (EToPMF) com Python')
print('====================================================================================================')
print('')
print('@authors    Isak Paulo de Andrade Ruas <isakruas@gmail.com>')
print('            Sibele Pinheiro da Silva <sibelepinheirosilva@gmail.com>')
print('')
print('@license    Este código é disponibilizado sobre a Licença Pública Geral (GNU) V3.0')
print('            Mais detalhes em: https://github.com/isakruas/EToPMF-Python/blob/master/LICENSE')
print('')
print('@link       Homepage:     https://isakruas.blogspot.com/2020/11/EToPMF-Python.html')
print('            GitHub Repo:  https://github.com/isakruas/EToPMF-Python/')
print('            README:       https://github.com/isakruas/EToPMF-Python/blob/master/README.md')
print('')
print('@version    1.0.00')
print('')

# Cálculo da pressão de saturação de vapor (e_s) em (kPa)

"""
    T = Temperatura média do ar (ºC)
    e_s = Pressão de saturação de vapor (kPa)
"""

T = input('Qual a temperatura média do ar (ºC)?\n')

e_s = 0.6108 * 10 ** ((7.5 * float(T)) / (237.3 + float(T)))

# Cálculo da pressão atual de vapor (e_a) em (kPa)

"""
    e_a = Pressão atual de vapor (kPa)
    UR = Umidade relativa média do ar (%)
"""
print('')

UR = input('Qual a umidade relativa média do ar (%)?\n')

e_a = (e_s * float(UR)) / 100

# Cálculo da distância inversa relativa entre a Terra e o Sol (dr) em (rad)

"""
    dr = Distância inversa relativa entre a Terra e o Sol (rad)
    J = Dia do ano
"""


def dia_do_ano(data_de_entrada):
    formato = '%d/%m/%Y'
    data = datetime.datetime.strptime(data_de_entrada, formato)
    data = data.timetuple()
    j = data.tm_yday
    ano = data.tm_year
    if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
        return j - 1
    else:
        return j


print('')

J = dia_do_ano(input('Qual é a data (d/m/Y)?\n'))

dr = 1 + 0.033 * math.cos((2 * math.pi / 365) * float(J))

# Cálculo da declinação sola (delta) em (rad)
"""
    delta = Declinação solar (rad)
"""

delta = 0.4093 * math.sin(((2 * math.pi) / 365) * J - 1.405)

# Cálculo da radiação solar no topo da atmosfera (Ra) em (MJm^-2dia^-1)

"""
    Ra = Radiação solar no topo da atmosfera (MJm^-2dia^-1)
    fi = Latitude do local (rad)
    omega_s = Ângulo horário ao nascer do Sol (rad)
"""

print('')

fi = input('Qual a latitude do local (rad)?\n')

omega_s = math.acos(-math.tan(float(fi)) * math.tan(float(delta)))

Ra = (118.08 / math.pi) * dr * (float(omega_s) * math.sin(float(fi)) * math.sin(float(delta)) + math.cos(float(fi)) * math.cos(float(delta)) * math.sin(float(omega_s)))

# Cálculo da radiação solar incidente na ausência de nuvens (Rso) em (MJm^-2dia^-1)

"""
    Rso = Radiação solar incidente na ausência de nuvens (MJm^-2dia^-1)
    z = Altitude (m)
"""

print('')

z = input('Qual a altitude (m)?\n')

Rso = (0.75 + float(z) * 2 * 10 ** -5) * Ra

# Cálculo do saldo de radiação de ondas longas (Rnl)

"""
    sigma = Constante de Stefan-Boltzmann (MJm^-2dia^-1)
    Tmax = Temperatura máxima do dia (ºC)
    Tmin = Temperatura mínima do dia (ºC)
    Rs =  Radiação solar incidente (MJm^-2dia^-1)    
"""

sigma = 4.903 * 10 ** -9

print('')

Tmax = input('Qual a temperatura máxima do dia (ºC)?\n')

print('')

Tmin = input('Qual a temperatura mínima do dia (ºC)?\n')

print('')

Rs = input('Qual radiação solar incidente (Rs) (MJm^-2dia^-1)?\n')

if not Rs:
    print('A radiação solar incidente (Rs) não foi informada')
    print('A radiação solar incidente (Rs) será calculada com base na radiação solar no topo da atmosfera, '
          'temperatura maxima e temperatura minima com coeficiente empírico igual a 0.16 para regiões continentais')
    Rs = 0.16 * float(Ra) * math.sqrt((float(Tmax) - float(Tmin)))
    pass

Rnl = sigma * (((float(Tmax) + 273.16) ** 4 + (float(Tmin) + 273.16) ** 4) / 2) * (0.34 - 0.14 * math.sqrt(e_a)) * (1.35 * (float(Rs) / float(Rso)) - 0.35)

# Cálculo do saldo de radiação de ondas curtas (Rns)

"""
    Rs   = Radiação solar incidente (MJm^-2dia^-1)
    alfa = Coeficiente de reflexão da vegetação (albedo)
"""

print('')

alfa = input('Qual o coeficiente de reflexão da vegetação (albedo)?\n')

if not alfa:
    print('O coeficiente de reflexão da vegetação (albedo) não foi informado')
    print('O coeficiente de reflexão da vegetação (albedo) será considerado como 0.23 para a cultura de referência de '
          'grama')
    alfa = 0.23
    pass

Rns = (1 - float(alfa)) * float(Rs)

# Estimativa do saldo de radiação (Rn)

"""
    Rn 	= Saldo de radiação
    Rns = Saldo de radiação de ondas curtas (MJm^-2dia^-1)
    Rnl = Saldo de radiação de ondas longas (MJm^-2dia^-1) 
"""
Rn = Rns - Rnl

#  Cálculo do fluxo de calor no solo (G)

"""
    G = Fluxo de calor no solo 
"""

print('')

G = input('Qual o fluxo total diário de calor no solo (G) (MJm^-2dia^-1)?\n')

if not G:
    print('O fluxo total diário de calor no solo (G) não foi informado')
    print('O fluxo total diário de calor no solo (G) será considerado como 0')
    G = 0
    pass

print('')

U_2 = input('Qual a velocidade do vento a 2m de altura  (U_2) (ms^-1)?\n')

if not U_2:
    print('A velocidade do vento a 2m de altura (U_2) não foi informada')
    print('A velocidade do vento a 2m de altura (U_2) será considerado como 2ms^-1')
    U_2 = 2.0
    pass

# Calculo da declividade da curva de pressão de vapor em relação à temperatura (Delta) (kPaºC^-1)

"""
    Delta = Declividade da curva de pressão de vapor em relação à temperatura
"""

Delta = (4098 * (0.6108 * 2.71828 ** ((17.27 * float(T)) / (float(T) + 237.3)))) / (float(T) + 237.3) ** 2

# Calculo da pressão atmosférica local (Patm) (kPa)

"""
    Patm = Pressão atmosférica local (kPa)
"""

Patm = 101.3 * ((293 - 0.0065 * float(z)) / 293) ** 5.26

# Calculo do coeficiente psicrométrico (gama) (kPaºC^-1)

"""
    gama = Coeficiente psicrométrico (kPaºC^-1)
"""

gama = Patm * 0.665 * 10 ** -3

# Estimativa de ETo pelo método de Penman-Monteith-FAO (EToPMF)

EToPMF = (0.408 * float(Delta) * (float(Rn) - float(G)) + (
            float(gama) * 900 * float(U_2) * (float(e_s) - float(e_a))) / (float(T) + 273)) / (
                     float(Delta) + float(gama) * (1 + 0.34 * float(U_2)))

print('')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Temperatura média do ar (ºC)                                                         | {T}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Pressão de saturação de vapor (kPa)                                                  | {e_s}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Pressão atual de vapor (kPa)                                                         | {e_a}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Umidade relativa média do ar (%)                                                     | {UR}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Distância inversa relativa entre a Terra e o Sol (rad)                               | {dr}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Dia do ano                                                                           | {J}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Declinação solar (rad)                                                               | {delta}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Radiação solar no topo da atmosfera (Ra) (MJm^-2dia^-1)                              | {Ra}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Latitude do local (rad)                                                              | {fi}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Ângulo horário ao nascer do Sol (rad)                                                | {omega_s}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Radiação solar incidente na ausência de nuvens (Rso) (MJm^-2dia^-1)                  | {Rso}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Altitude (m)                                                                         | {z}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Constante de Stefan-Boltzmann (MJm^-2dia^-1)                                         | {sigma}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Temperatura máxima do dia (ºC)                                                       | {Tmax}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Temperatura mínima do dia (ºC)                                                       | {Tmin}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Radiação solar incidente (Rs) (MJm^-2dia^-1)                                         | {Rs}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Coeficiente de reflexão da vegetação (albedo)                                        | {alfa}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Saldo de radiação (Rn)                                                               | {Rn}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Saldo de radiação de ondas curtas (Rns) (MJm^-2dia^-1)                               | {Rns}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Saldo de radiação de ondas longas (Rnl) (MJm^-2dia^-1)                               | {Rnl}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Fluxo total diário de calor no solo (G)                                              | {G}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Velocidade do vento a 2m de altura (U_2)                                             | {U_2}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Declividade da curva de pressão de vapor em relação à temperatura (Delta) (kPaºC^-1) | {Delta}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Pressão atmosférica local (Patm) (kPa)                                               | {Patm}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| Coeficiente psicrométrico (gama) (kPaºC^-1)                                          | {gama}')
print(
    '|---------------------------------------------------------------------------------------------------------------')
print(f'| EToPMF                                                                               | {EToPMF}')
print(
    '|---------------------------------------------------------------------------------------------------------------')