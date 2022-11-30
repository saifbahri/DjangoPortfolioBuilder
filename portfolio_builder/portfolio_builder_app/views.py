import datetime , jwt
from rest_framework.decorators import api_view
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse

from .authentification import decode_auth_token
from portfolio_builder_app.serializers import *
from .models import *


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('email failed failed')

        payload = {
            'id': user.id,
            'role':user.role, 
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret', algorithm='HS256').encode('utf-8')

        if user.check_password(password):
            return Response({'JWT': token})
        else:
            raise AuthenticationFailed('login failed')








####################################################### CRUD USER ###################################################

@api_view(['GET'])
def get_all_Users(request):
    auth = get_authorization_header(request).split()
    if auth and len(auth) == 2:
        if request.method=='GET':
            token = auth[1].decode('utf-8')
            role = decode_auth_token(token)
            if role == 1:
                users=User.objects.all() 
                if  not users: 
                    return Response(status=status.HTTP_204_NO_CONTENT)
                serializer=UserSerializer(users,many=True) 
                return Response(serializer.data,status=status.HTTP_200_OK)
            raise AuthenticationFailed('only for admin')   
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    raise AuthenticationFailed('unauthorized')    

@api_view(['GET'])
def getusertByID(request,id): 
    auth = get_authorization_header(request).split()
    if auth and len(auth) == 2:     
        if request.method=='GET':
            
                user = User.objects.get(pk=id)
                serializer = UserSerializer(user, many=False)
                return JsonResponse(serializer.data, safe=False)
            
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    raise AuthenticationFailed('unauthorized') 

@api_view(['POST'])
def add_User(request):
    auth = get_authorization_header(request).split()
    if auth and len(auth) == 2:

        if request.method=='POST':
            user=UserSerializer(data=request.data) 
            if user.is_valid(): 
                user.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(user.errors,status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    raise AuthenticationFailed('unauthorized')    



@api_view(['DELETE'])
def delete_user(request,id):
    auth = get_authorization_header(request).split()
    if auth and len(auth) == 2:               
        if request.method=='DELETE':
           token = auth[1].decode('utf-8')
           role = decode_auth_token(token)
           if role == 1: 
                try:
                    user=User.objects.get(pk=id)
                    user.delete()
                    return JsonResponse({"message": "the User has been successfuly removed."},status=status.HTTP_202_ACCEPTED)
                except user.DoesNotExist: 
                    return Response(status=status.HTTP_404_NOT_FOUND)       
           raise AuthenticationFailed('only for admin')       
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    raise AuthenticationFailed('unauthorized')    



@api_view(['PUT'])
def modify_User(request,id):
   auth = get_authorization_header(request).split()
   if auth and len(auth) == 2:                 
    if request.method=='PUT':
        try:
         user=User.objects.get(pk=id)   
         serializer=UserSerializer(user,data=request.data)
         if serializer.is_valid():
          serializer.save()
         return Response(status=status.HTTP_202_ACCEPTED)
        except user.DoesNotExist: 
         return Response(status=status.HTTP_404_NOT_FOUND)     
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   raise AuthenticationFailed('unauthorized') 





####################################################### CRUD PORTFOLIO ###################################################

@api_view(['GET'])
def get_all_Portfolios(request):
    auth = get_authorization_header(request).split()
    if auth and len(auth) == 2:            
           
        if request.method=='GET':
            Portfolios=Portfolio.objects.all() 
            if  not Portfolios: 
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer=PortfolioSerializer(Portfolios,many=True) 
            return Response(serializer.data,status=status.HTTP_200_OK)
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    raise AuthenticationFailed('unauthorized') 


@api_view(['GET'])
def getportfolioByID(request,id):
    auth = get_authorization_header(request).split()
    if auth and len(auth) == 2:

        if request.method=='GET':
                portfolio = Portfolio.objects.get(pk=id)
                serializer = PortfolioSerializer(portfolio, many=False)
                return JsonResponse(serializer.data, safe=False)
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    raise AuthenticationFailed('unauthorized')

    
@api_view(['POST'])
def add_Portfolio(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:
        if request.method=='POST':
            portfolio=PortfolioSerializer(data=request.data) 
            if portfolio.is_valid(): 
                portfolio.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(portfolio.errors,status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')


@api_view(['DELETE'])
def delete_protfolio(request,id):
    auth = get_authorization_header(request).split()
    if auth and len(auth) == 2:               
        if request.method=='DELETE':
            try:
                portfolio=Portfolio.objects.get(pk=id)
                portfolio.delete()
                return JsonResponse({"message": "the Portfolio has been successfuly removed."},status=status.HTTP_202_ACCEPTED)
            except portfolio.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)       
            
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@api_view(['PUT'])
def modify_portfolio(request,id):
 auth = get_authorization_header(request).split()
 if auth and len(auth) == 2:
    if request.method=='PUT':
        try:
         portfolio=Portfolio.objects.get(pk=id)   
         serializer=PortfolioSerializer(portfolio,data=request.data)
         if serializer.is_valid():
          serializer.save()
         return Response(status=status.HTTP_202_ACCEPTED)
        except portfolio.DoesNotExist: 
         return Response(status=status.HTTP_404_NOT_FOUND)     
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
 raise AuthenticationFailed('unauthorized')  


####################################################### CRUD BIOGRAPHY ###################################################

@api_view(['GET'])
def get_all_Biography(request):

 auth = get_authorization_header(request).split()
 if auth and len(auth) == 2:  
    if request.method=='GET':
        biographies=Biography.objects.all() 
        if  not biographies: 
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer=BiographySerializer(biographies,many=True) 
        return Response(serializer.data,status=status.HTTP_200_OK)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
 raise AuthenticationFailed('unauthorized')




@api_view(['GET'])
def getbioByID(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:
    if request.method=='GET':
        
            bio = Biography.objects.get(pk=id)
            serializer = BiographySerializer(bio, many=False)
            return JsonResponse(serializer.data, safe=False)
       
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')

@api_view(['POST'])
def add_Biography(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:  
    if request.method=='POST':
        biography=BiographySerializer(data=request.data) 
        if biography.is_valid(): 
            biography.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(Biography.errors,status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')  



@api_view(['DELETE'])
def delete_Biography(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:                 
        if request.method=='DELETE': 
            try:
                biography=Biography.objects.get(pk=id)
                biography.delete()
                return JsonResponse({"message": "the Biography has been successfuly removed."},status=status.HTTP_202_ACCEPTED)
            except biography.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)       
            
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized') 


@api_view(['PUT'])
def modify_Biography(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:   
    if request.method=='PUT':
        try:
         biography=Biography.objects.get(pk=id)   
         serializer=BiographySerializer(biography,data=request.data)
         if serializer.is_valid():
          serializer.save()
         return Response(status=status.HTTP_202_ACCEPTED)
        except biography.DoesNotExist: 
         return Response(status=status.HTTP_404_NOT_FOUND)     
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  raise AuthenticationFailed('unauthorized')  






####################################################### CRUD SOCIAL MEDIA ###################################################

@api_view(['GET'])
def get_all_socialmedias(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:
    if request.method=='GET':
        medias=social_media.objects.all() 
        if  not medias: 
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer=social_mediaSerializer(medias,many=True) 
        return Response(serializer.data,status=status.HTTP_200_OK)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')   



@api_view(['GET'])
def getmediaByID(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:  
    if request.method=='GET':
       
            media = social_media.objects.get(pk=id)
            serializer = social_mediaSerializer(media, many=False)
            return JsonResponse(serializer.data, safe=False)
        
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')   

@api_view(['POST'])
def add_social_media(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:  
    if request.method=='POST':
        media=social_mediaSerializer(data=request.data) 
        if media.is_valid(): 
            media.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(social_media.errors,status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')   


@api_view(['DELETE'])
def delete_social_media(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:               
        if request.method=='DELETE': 
            try:
                media=social_media.objects.get(pk=id)
                media.delete()
                return JsonResponse({"message": "the Biography has been successfuly removed."},status=status.HTTP_202_ACCEPTED)
            except media.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)       
            
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')  


@api_view(['PUT'])
def modify_social_media(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:      
    if request.method=='PUT':
        try:
         media=social_media.objects.get(pk=id)   
         serializer=social_mediaSerializer(media,data=request.data)
         if serializer.is_valid():
          serializer.save()
         return Response(status=status.HTTP_202_ACCEPTED)
        except media.DoesNotExist: 
         return Response(status=status.HTTP_404_NOT_FOUND)     
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  raise AuthenticationFailed('unauthorized')  



####################################################### CRUD PROFESSIONAL ACCOMPLISHMENT ###################################################

@api_view(['GET'])
def get_all_accomps(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:   
    if request.method=='GET':
        pros=professional_accomplishment.objects.all() 
        if  not pros: 
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer=professional_accomplishmentSerializer(pros,many=True) 
        return Response(serializer.data,status=status.HTTP_200_OK)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')


@api_view(['GET'])
def getaccompByID(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:  
    if request.method=='GET':
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            accomp = professional_accomplishment.objects.get(pk=id)
            serializer = professional_accomplishmentSerializer(accomp, many=False)
            return JsonResponse(serializer.data, safe=False)
        
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')


@api_view(['POST'])
def add_professional_accomp(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:     
    if request.method=='POST':
        professional_accomp=professional_accomplishmentSerializer(data=request.data) 
        if professional_accomp.is_valid(): 
            professional_accomp.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(professional_accomplishment.errors,status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')


@api_view(['DELETE'])
def delete_professional_accomplishment(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:     
                   
        if request.method=='DELETE': 
            try:
                professional_accomp=professional_accomplishment.objects.get(pk=id)
                professional_accomp.delete()
                return JsonResponse({"message": "the Biography has been successfuly removed."},status=status.HTTP_202_ACCEPTED)
            except professional_accomp.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)       
            
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')


@api_view(['PUT'])
def modify_professional_accomplishment(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:     
    if request.method=='PUT':

        try:
         accomp=professional_accomplishment.objects.get(pk=id)   
         serializer=professional_accomplishmentSerializer(accomp,data=request.data)
         if serializer.is_valid():
          serializer.save()
         return Response(status=status.HTTP_202_ACCEPTED)
        except accomp.DoesNotExist: 
         return Response(status=status.HTTP_404_NOT_FOUND)     
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  raise AuthenticationFailed('unauthorized')



####################################################### CRUD AWARD ###################################################

@api_view(['GET'])
def get_all_awards(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:   
    if request.method=='GET':
        awards=award.objects.all() 
        if  not awards: 
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer=professional_accomplishmentSerializer(awards,many=True) 
        return Response(serializer.data,status=status.HTTP_200_OK)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')

@api_view(['GET'])
def getawardByID(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:  
    if request.method=='GET':
        
            Award = award.objects.get(pk=id)
            serializer = awardSerializer(Award, many=False)
            return JsonResponse(serializer.data, safe=False)
        
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')

@api_view(['POST'])
def add_award(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:   
    if request.method=='POST':
        Award=awardSerializer(data=request.data) 
        if Award.is_valid(): 
            Award.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(award.errors,status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')

@api_view(['DELETE'])
def delete_award(request,id):
    auth = get_authorization_header(request).split()
    if auth and len(auth) == 2:                
        if request.method=='DELETE': 
            try:
                Award=award.objects.get(pk=id)
                Award.delete()
                return JsonResponse({"message": "the Biography has been successfuly removed."},status=status.HTTP_202_ACCEPTED)
            except Award.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)       
            
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    raise AuthenticationFailed('unauthorized')


@api_view(['PUT'])
def modify_award(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:   
    if request.method=='PUT':
        try:
         Award=award.objects.get(pk=id)   
         serializer=awardSerializer(Award,data=request.data)
         if serializer.is_valid():
          serializer.save()
         return Response(status=status.HTTP_202_ACCEPTED)
        except Award.DoesNotExist: 
         return Response(status=status.HTTP_404_NOT_FOUND)     
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  raise AuthenticationFailed('unauthorized')  


####################################################### CRUD JUSTIFICATION ###################################################

@api_view(['GET'])
def get_all_justifications(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:     
    if request.method=='GET':
        justifications=justification.objects.all() 
        if  not justifications: 
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer=justificationSerializer(justifications,many=True) 
        return Response(serializer.data,status=status.HTTP_200_OK)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')

@api_view(['GET'])

def getjustificationByID(request,id):
   auth = get_authorization_header(request).split()
   if auth and len(auth) == 2:  
    if request.method=='GET':
       
            Justification = justification.objects.get(pk=id)
            serializer = justificationSerializer(Justification, many=False)
            return JsonResponse(serializer.data, safe=False)
        
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
   raise AuthenticationFailed('unauthorized')  

@api_view(['POST'])
def add_justification(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:     
    if request.method=='POST':
        Justification=justificationSerializer(data=request.data) 
        if Justification.is_valid(): 
            Justification.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(award.errors,status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')


@api_view(['DELETE'])
def delete_justificaiton(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:                  
        if request.method=='DELETE': 
            try:
                Justification=justification.objects.get(pk=id)
                Justification.delete()
                return JsonResponse({"message": "the Biography has been successfuly removed."},status=status.HTTP_202_ACCEPTED)
            except Justification.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)       
            
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')


@api_view(['PUT'])
def modify_justification(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:     
    if request.method=='PUT':
        try:
         Justification=justification.objects.get(pk=id)   
         serializer=justificationSerializer(Justification,data=request.data)
         if serializer.is_valid():
          serializer.save()
         return Response(status=status.HTTP_202_ACCEPTED)
        except Justification.DoesNotExist: 
         return Response(status=status.HTTP_404_NOT_FOUND)     
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  raise AuthenticationFailed('unauthorized')


####################################################### CRUD CERTIFICATION ###################################################

@api_view(['GET'])
def get_all_certifications(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:    
    if request.method=='GET':
        certifications=certification.objects.all() 
        if  not certifications: 
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer=certificationSerializer(certifications,many=True) 
        return Response(serializer.data,status=status.HTTP_200_OK)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')

@api_view(['GET'])
def getcertificationByID(request,id):
   auth = get_authorization_header(request).split()
   if auth and len(auth) == 2:  
    if request.method=='GET':
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            certif = certification.objects.get(pk=id)
            serializer = certificationSerializer(certif, many=False)
            return JsonResponse(serializer.data, safe=False)
        
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
   raise AuthenticationFailed('unauthorized')

@api_view(['POST'])
def add_certification(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:    
    if request.method=='POST':
        Certification=certificationSerializer(data=request.data) 
        if  Certification.is_valid(): 
            Certification.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(award.errors,status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')


@api_view(['DELETE'])
def delete_certification(request,id):

     auth = get_authorization_header(request).split()
     if auth and len(auth) == 2:                 
        if request.method=='DELETE': 
            try:
                Certification= certification.objects.get(pk=id)
                Certification.delete()
                return JsonResponse({"message": "the Biography has been successfuly removed."},status=status.HTTP_202_ACCEPTED)
            except Certification.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)       
            
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
     raise AuthenticationFailed('unauthorized')


@api_view(['PUT'])
def modify_certification(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:    
    if request.method=='PUT':
        try:
         Certification=certification.objects.get(pk=id)   
         serializer=certificationSerializer(Certification,data=request.data)
         if serializer.is_valid():
          serializer.save()
         return Response(status=status.HTTP_202_ACCEPTED)
        except Certification.DoesNotExist: 
         return Response(status=status.HTTP_404_NOT_FOUND)     
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  raise AuthenticationFailed('unauthorized') 



####################################################### CRUD COMMUNITY SERVICE ###################################################

@api_view(['GET'])
def get_all_cservices(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:   
    if request.method=='GET':
        cservices=community_service.objects.all() 
        if  not cservices: 
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer=community_serviceSerializer(cservices,many=True) 
        return Response(serializer.data,status=status.HTTP_200_OK)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized') 

@api_view(['GET'])
def getcserviceByID(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:  
    if request.method=='GET':
        
            cservice = community_service.objects.get(pk=id)
            serializer = community_serviceSerializer(cservice, many=False)
            return JsonResponse(serializer.data, safe=False)
        
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized')

@api_view(['POST'])
def add_community_service(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:   
    if request.method=='POST':
        c_service=community_serviceSerializer(data=request.data) 
        if  c_service.is_valid(): 
            c_service.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(award.errors,status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized') 


@api_view(['DELETE'])
def delete_community_service(request,id):
   auth = get_authorization_header(request).split()
   if auth and len(auth) == 2:  
                   
        if request.method=='DELETE': 
            try:
                c_service= community_service.objects.get(pk=id)
                c_service.delete()
                return JsonResponse({"message": "the Biography has been successfuly removed."},status=status.HTTP_202_ACCEPTED)
            except c_service.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)       
            
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
   raise AuthenticationFailed('unauthorized') 


@api_view(['PUT'])
def modify_community_service(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:   
    if request.method=='PUT':
        try:
         cservice=community_service.objects.get(pk=id)   
         serializer=community_serviceSerializer(cservice,data=request.data)
         if serializer.is_valid():
          serializer.save()
         return Response(status=status.HTTP_202_ACCEPTED)
        except cservice.DoesNotExist: 
         return Response(status=status.HTTP_404_NOT_FOUND)     
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  raise AuthenticationFailed('unauthorized') 



####################################################### CRUD REFRENCE ###################################################

@api_view(['GET'])
def get_all_references(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:     
    if request.method=='GET':
        references=reference.objects.all() 
        if  not references: 
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer=referenceSerializer(references,many=True) 
        return Response(serializer.data,status=status.HTTP_200_OK)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized') 

@api_view(['GET'])
def getrefByID(request,id):
   auth = get_authorization_header(request).split()
   if auth and len(auth) == 2:  
    if request.method=='GET':
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            ref = reference.objects.get(pk=id)
            serializer = referenceSerializer(ref, many=False)
            return JsonResponse(serializer.data, safe=False)
        
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
   raise AuthenticationFailed('unauthorized')


@api_view(['POST'])
def add_reference(request):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:     
    if request.method=='POST':
        ref=referenceSerializer(data=request.data) 
        if  ref.is_valid(): 
            ref.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(award.errors,status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized') 


@api_view(['DELETE'])
def delete_reference(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:   
                   
        if request.method=='DELETE': 
            try:
                ref= reference.objects.get(pk=id)
                ref.delete()
                return JsonResponse({"message": "the Biography has been successfuly removed."},status=status.HTTP_202_ACCEPTED)
            except ref.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND)       
            
        return JsonResponse({"message":"The method is not allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  raise AuthenticationFailed('unauthorized') 


@api_view(['PUT'])
def modify_reference(request,id):
  auth = get_authorization_header(request).split()
  if auth and len(auth) == 2:     
    if request.method=='PUT':
        try:
         Reference=reference.objects.get(pk=id)   
         serializer=referenceSerializer(Reference,data=request.data)
         if serializer.is_valid():
          serializer.save()
         return Response(status=status.HTTP_202_ACCEPTED)
        except Reference.DoesNotExist: 
         return Response(status=status.HTTP_404_NOT_FOUND)     
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  raise AuthenticationFailed('unauthorized') 