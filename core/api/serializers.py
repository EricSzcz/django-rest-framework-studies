from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from atracoes.models import Atracao
from core.models import PontoTuristico
from atracoes.api.serializers import AtracaoSerializer
from enderecos.api.serializers import EnderecoSerializer
from avaliacoes.api.serializers import AvaliacaoSerializer
from comentarios.api.serializers import ComentarioSerializer
from enderecos.models import Endereco

"""
Incluindo outros serializers no retorno do principal
"""


class PontoTuristicoSerializer(ModelSerializer):
    atracoes = AtracaoSerializer(many=True)
    endereco = EnderecoSerializer(read_only=True)
    #avaliacoes = AvaliacaoSerializer(many=True)
    #comentarios = ComentarioSerializer(many=True)
    descricao_completa = SerializerMethodField()

    class Meta:
        model = PontoTuristico
        fields = ('id', 'nome', 'descricao', 'aprovado', 'foto',
                  'atracoes', 'comentarios', 'avaliacoes', 'endereco',
                  'descricao_completa', 'descricao_completa2'
        )

        read_only_fields = ('comentarios', 'avaliacoes')

    def cria_atracoes(self, atracoes, ponto):
        for atracao in atracoes:
            at = Atracao.objects.create(**atracao)
            ponto.atracoes.add(at)


    def create(self, validated_data):
        atracoes = validated_data['atracoes']
        del validated_data['atracoes']

        ponto = PontoTuristico.objects.create(**validated_data)
        self.cria_atracoes(atracoes, ponto)

        return ponto

    """
    forma de manipular dados antes de enviar o retorno (metodo nao recomendado)
    """


    def get_descricao_completa(self, obj):
        return '%s - %s' % (obj.nome, obj.descricao)
