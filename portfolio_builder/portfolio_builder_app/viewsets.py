
from portfolio_builder_app.serializers import *
from rest_framework import viewsets
from .models import *






    
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_name = ['get', 'post', 'put','delete','patch']



class BiographyViewSet(viewsets.ModelViewSet):

    queryset = Biography.objects.all()
    serializer_class = BiographySerializer
    http_method_name = ['get', 'post', 'put', 'delete','patch']

    
class social_mediaViewSet(viewsets.ModelViewSet):

    queryset = social_media.objects.all()
    serializer_class = social_mediaSerializer
    http_method_name = ['get', 'post', 'put', 'delete','patch']


class PortfolioViewSet(viewsets.ModelViewSet):

    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    http_method_name = ['get', 'post', 'put', 'delete','patch']



class professional_accomplishmentViewSet(viewsets.ModelViewSet):

    queryset = professional_accomplishment.objects.all()
    serializer_class = professional_accomplishmentSerializer
    http_method_name = ['get', 'post', 'put', 'delete','patch']



class awardViewSet(viewsets.ModelViewSet):

    queryset = award.objects.all()
    serializer_class = awardSerializer
    http_method_name = ['get', 'post', 'put', 'delete','patch']

    
class justificationViewSet(viewsets.ModelViewSet):

    queryset =justification.objects.all()
    serializer_class =justificationSerializer
    http_method_name = ['get', 'post', 'put', 'delete','patch']



class certificationViewSet(viewsets.ModelViewSet):

    queryset = certification.objects.all()
    serializer_class = certificationSerializer
    http_method_name = ['get', 'post', 'put', 'delete','patch']


class community_serviceViewSet(viewsets.ModelViewSet):

    queryset = community_service.objects.all()
    serializer_class = community_serviceSerializer
    http_method_name = ['get', 'post', 'put', 'delete','patch']

    
class referenceViewSet(viewsets.ModelViewSet):

    queryset = reference.objects.all()
    serializer_class = referenceSerializer
    http_method_name = ['get', 'post', 'put', 'delete','patch']
