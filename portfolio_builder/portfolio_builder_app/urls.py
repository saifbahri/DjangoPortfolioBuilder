from django.urls import include,path
from rest_framework import routers
from portfolio_builder_app import views
#urls using ModelViewSet
from portfolio_builder_app.viewsets import *
router=routers.DefaultRouter() #get the default router object defined in rest_framework
#add router for each viewset (userViewest, portfolioViewSet, roleViewSet) to the router object
router.register(r'users',UserViewSet) 
#each time we use the path '/users' in the url, 
#the StudentViewSet will be called
#the prefix r is used to indicate that the string is a raw string (not interpret the backslash as an escape character)


router.register(r'biographies',BiographyViewSet)
router.register(r'social_medais',social_mediaViewSet)
router.register(r'portfolios',PortfolioViewSet)
router.register(r'pros',professional_accomplishmentViewSet)
router.register(r'awards',awardViewSet)
router.register(r'justifications',justificationViewSet)
router.register(r'certifications',certificationViewSet)
router.register(r'cservices',community_serviceViewSet)
router.register(r'references',referenceViewSet)
# #add the router to the urlpatterns
# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = [
    path('user/login/',views.LoginView.as_view()),
     path('', include(router.urls)),
    
    path(r'user/all/',views.get_all_Users),
    path(r'user/getuserbyid/<int:id>',views.getusertByID),
    path(r'user/add/',views.add_User),
    path(r'user/delete/<int:id>',views.delete_user),
    path(r'user/modify/<int:id>',views.modify_User),


    path(r'bio/all/',views.get_all_Biography),
    path(r'bio/getbiobyid/<int:id>',views.getbioByID),
    path(r'bio/add/',views.add_Biography),
    path(r'bio/delete/<int:id>',views.delete_Biography),
    path(r'bio/modify/<int:id>',views.modify_Biography),


    path(r'portfolio/all/',views.get_all_Portfolios),
    path(r'portfolio/getportfoliobyid/<int:id>',views.getportfolioByID),
    path(r'portfolio/add/',views.add_Portfolio),
    path(r'portfolio/delete/<int:id>',views.delete_protfolio),
    path(r'portfolio/modify/<int:id>',views.modify_portfolio),

    
    path(r'media/all/',views.get_all_socialmedias),
    path(r'media/getmediabyid/<int:id>',views.getmediaByID),
    path(r'media/add/',views.add_social_media),
    path(r'media/delete/<int:id>',views.delete_social_media),
    path(r'media/modify/<int:id>',views.modify_social_media),
    
    
    path(r'award/all/',views.get_all_awards),
    path(r'award/getawaardbyid/<int:id>',views.getawardByID),
    path(r'award/add/',views.add_award),
    path(r'award/delete/<int:id>',views.delete_award),
    path(r'award/modify/<int:id>',views.modify_award),


    path(r'justification/all/',views.get_all_justifications),
    path(r'justification/getjustificationbyid/<int:id>',views.getjustificationByID),
    path(r'justification/add/',views.add_justification),
    path(r'justification/delete/<int:id>',views.delete_justificaiton),
    path(r'justification/modify/<int:id>',views.modify_justification),


    path(r'certification/all/',views.get_all_certifications),
    path(r'certification/getcertificationbyid/<int:id>',views.getcertificationByID),
    path(r'certification/add/',views.add_certification),
    path(r'certification/delete/<int:id>',views.delete_certification),
    path(r'certification/modify/<int:id>',views.modify_certification),


    path(r'cservice/all/',views.get_all_cservices),
    path(r'cservice/getcservicebyid/<int:id>',views.getcserviceByID),
    path(r'cservice/add/',views.add_community_service),
    path(r'cservice/delete/<int:id>',views.delete_community_service),
    path(r'cservice/modify/<int:id>',views.modify_community_service),


    path(r'reference/all/',views.get_all_references),
    path(r'reference/getreferencebyid/<int:id>',views.getrefByID),
    path(r'reference/add/',views.add_reference),
    path(r'reference/delete/<int:id>',views.delete_reference),
    path(r'reference/modify/<int:id>',views.modify_reference),
]

