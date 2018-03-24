from apps.senator.models import (Parliamentarian, Mandate, Alternate, Exercise)

__author__ = "Gilson Paulino"
__date__ = "Created by 24/03/18"
__copyright__ = "Copyright 2018"
__email__ = "gilsonbp@gmail.com"


class ImportSenatorJSON(object):
    """
    Importing parliamentarians through the endpoint (http://legis.senado.gov.br/dadosabertos/senador/lista/atual)
    """

    @staticmethod
    def parliamentarian(jsonresponse):
        """
        Method for importing parliamentarians
        :param jsonresponse: JSON containing the list of parliamentarians
        :return: Quantity of parliamentarians imported.
        """

        # Clears all parliamentarians and dependent tables before re-importing
        Parliamentarian.objects.all().delete()

        rows = 0

        # loop on the list of parliamentarians
        for pl in jsonresponse['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']:

            idp = pl.get('IdentificacaoParlamentar')
            if idp.get('CodigoParlamentar', False):  # Checking if there is a parliamentary code

                # Recording the handles in the database
                parliamentarian = Parlamentar.objects.create(
                    codigo=idp.get('CodigoParlamentar'),
                    nome=idp.get('NomeParlamentar', None),
                    nome_completo=idp.get('NomeCompletoParlamentar', None),
                    sexo=idp.get('SexoParlamentar', None),
                    forma_tratamento=idp.get('FormaTratamento', None),
                    url_foto=idp.get('UrlFotoParlamentar', None),
                    url_pagina=idp.get('UrlPaginaParlamentar', None),
                    email=idp.get('EmailParlamentar', None),
                    sigla_partido=idp.get('SiglaPartidoParlamentar', None),
                    uf=idp.get('UfParlamentar', None),
                    glossario=pl.get('UrlGlossario', None)
                )

                mdt = pl.get('Mandato', False)
                if mdt:  # Checking for Mandates
                    holder = mdt.get('Titular', False)
                    if holder:
                        t_descricao_participacao = holder.get(
                            'DescricaoParticipacao', None)
                        t_codigo_parlamentar = holder.get(
                            'CodigoParlamentar', None)
                        t_nome_parlamentar = holder.get(
                            'NomeParlamentar', None)
                    else:
                        t_descricao_participacao = None
                        t_codigo_parlamentar = None
                        t_nome_parlamentar = None

                    # Writing mandates to the database
                    mandate = Mandate.objects.create(
                        parliamentarian=parliamentarian,
                        codigo=mdt.get('CodigoMandato'),
                        uf=mdt.get('UfParlamentar', None),
                        pl_numero=mdt['PrimeiraLegislaturaDoMandato']['NumeroLegislatura'],
                        pl_data_inicio=mdt['PrimeiraLegislaturaDoMandato']['DataInicio'],
                        pl_data_fim=mdt['PrimeiraLegislaturaDoMandato']['DataFim'],
                        sl_numero=mdt['SegundaLegislaturaDoMandato']['NumeroLegislatura'],
                        sl_data_inicio=mdt['SegundaLegislaturaDoMandato']['DataInicio'],
                        sl_data_fim=mdt['SegundaLegislaturaDoMandato']['DataFim'],
                        descricao_participacao=mdt.get(
                            'DescricaoParticipacao', None),
                        t_descricao_participacao=t_descricao_participacao,
                        t_codigo_parlamentar=t_codigo_parlamentar,
                        t_nome_parlamentar=t_nome_parlamentar
                    )

                    alternates = mdt.get('Suplentes', False)
                    if alternates:  # checking whether they were Alternates
                        # Testing the Alternates data type, when there is only one return is one
                        if type(alternates.get('Suplente')) == dict:
                            supl = alternates.get('Suplente')
                            Alternate.objects.create(
                                mandate=mandate,
                                codigo_parlamentar=supl.get(
                                    'CodigoParlamentar'),
                                descricao_participacao=supl.get(
                                    'DescricaoParticipacao'),
                                nome_parlamentar=supl.get('NomeParlamentar'),
                            )
                        else:  # when there is more than one the return is a list
                            for supl in alternates.get('Suplente'):
                                Alternate.objects.create(
                                    mandate=mandate,
                                    codigo_parlamentar=supl.get(
                                        'CodigoParlamentar'),
                                    descricao_participacao=supl.get(
                                        'DescricaoParticipacao'),
                                    nome_parlamentar=supl.get(
                                        'NomeParlamentar'),
                                )

                    exercises = mdt.get('Exercicios', False)
                    if exercises:  # Checking if there are exercises
                        # Testing the exercise data type, when there is only one return is a dictionary
                        if type(exercises.get('Exercicio')) == dict:
                            exer = exercises.get('Exercicio')
                            Exercise.objects.create(
                                mandate=mandate,
                                codigo=exer.get('CodigoExercicio'),
                                data_inicio=exer.get('DataInicio'),
                                data_fim=exer.get('DataFim'),
                                sigla_causa_afastamento=exer.get(
                                    'SiglaCausaAfastamento'),
                                descricao_causa_afastamento=exer.get(
                                    'DescricaoCausaAfastamento'),
                                data_leitura=exer.get('DataLeitura'),
                            )
                        else:  # when there is more than one the return is a list
                            for exer in exercises.get('Exercicio'):
                                Exercise.objects.create(
                                    mandate=mandate,
                                    codigo=exer.get('CodigoExercicio'),
                                    data_inicio=exer.get('DataInicio'),
                                    data_fim=exer.get('DataFim'),
                                    sigla_causa_afastamento=exer.get(
                                        'SiglaCausaAfastamento'),
                                    descricao_causa_afastamento=exer.get(
                                        'DescricaoCausaAfastamento'),
                                    data_leitura=exer.get('DataLeitura'),
                                )

                rows += 1

        return rows
