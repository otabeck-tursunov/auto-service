from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *
from rest_framework.views import APIView

from .serializers import *

from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token payload
        token['id'] = user.id
        token['username'] = user.username
        token['password'] = user.password
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny, ]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        refresh = serializer.validated_data.get('refresh')
        access = serializer.validated_data.get('access')

        # Hashlanmagan parolni qaytarish
        raw_password = request.data.get('password')

        # Add custom fields to the response
        data = {
            'refresh': str(refresh),
            'access': str(access),
            'id': user.id,
            'username': user.username,
            'password': raw_password,  # Hashlanmagan parol
        }
        return Response(data)


class UsersListAPIView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['username', ]
    search_fields = ['username', ]


from django.contrib.auth.hashers import make_password


class UserAPIView(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            if password:
                serializer.validated_data['password'] = make_password(password)  # Parolni hashlash
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Oldingi muvaffaqiyatsizlik xabarlarni yo'q qilish
            serializer._errors = {}

            # `is_staff` va `is_active` qiymatlarini sozlangan to'g'ri ishlovchi foydalanuvchini saqlash
            user = serializer.save(is_staff=True, is_active=True)

            # Parolni o'zgartirish
            password = request.data.get('password')
            if password:
                user.set_password(password)
                user.save()

            return Response({'message': 'Ma\'lumotlaringiz muvaffaqiyatli o\'zgartirildi.'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MahsulotTurlariListCreateAPIView(ListCreateAPIView):
    queryset = Mahsulot_turi.objects.all()
    serializer_class = MahsulotTuriSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['nom', ]
    search_fields = ['nom', ]


class MahsulotTuriDetailsAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Mahsulot_turi.objects.all()
    serializer_class = MahsulotTuriSerializer


class MahsulotlarListCreateAPIView(APIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['nom', 'sana', 'turi__nom']
    search_fields = ['nom', ]
    @swagger_auto_schema(

        manual_parameters=[
            openapi.Parameter(
                name='turi_id',
                in_=openapi.IN_QUERY,
                description='Mahsulot turi ID-si',
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def get(self, request):
        turi_id = request.GET.get('turi_id')

        if turi_id is not None:
            mahsulotlar = Mahsulot.objects.filter(turi_id=turi_id)
        else:
            mahsulotlar = Mahsulot.objects.all()

        serializer = MahsulotSerializer(mahsulotlar, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=MahsulotSerializer,
        operation_description="Create a new Mahsulot instance",
        # responses={status.HTTP_201_CREATED: MahsulotSerializer}
    )
    def post(self, request):
        serializer = MahsulotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MahsulotDetailsAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Mahsulot.objects.all()
    serializer_class = MahsulotSerializer


class MijozlarListCreateAPIView(ListCreateAPIView):
    queryset = Mijoz.objects.all()
    serializer_class = MijozSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['avtomobil', ]
    search_fields = ['avtomobil', 'avto_raqam']

    pagination_class = PageNumberPagination
    # Set the desired page size
    page_size = 10


class MijozDetailsAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Mijoz.objects.all()
    serializer_class = MijozSerializer


class SavdolarListCreateAPIView(ListCreateAPIView):
    queryset = Savdo.objects.all()
    serializer_class = SavdoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['mahsulot__nom', 'mijoz__avtomobil', 'summa', 'miqdor']
    search_fields = ['mahsulot__nom', 'mijoz__avtomobil']

    pagination_class = PageNumberPagination
    # Set the desired page size
    page_size = 10


class SavdoDetailsAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Savdo.objects.all()
    serializer_class = SavdoSerializer


class ChiqimlarListCreateAPIView(ListCreateAPIView):
    queryset = Chiqim.objects.all()
    serializer_class = ChiqimSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['summa', 'masul', 'sana']
    search_fields = ['masul']

    pagination_class = PageNumberPagination
    # Set the desired page size
    page_size = 10


class ChiqimDetailsAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Chiqim.objects.all()
    serializer_class = ChiqimSerializer


class StatsAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="start_date",
                in_=openapi.IN_QUERY,
                description="Boshlang'ich sanaga (YYYY-MM-DD) ko'ra statistikani filtrlash",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
            openapi.Parameter(
                name="end_date",
                in_=openapi.IN_QUERY,
                description="Oxirgi sanaga (YYYY-MM-DD) ko'ra statistikani filtrlash",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
        ],
    )
    def get(self, request):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            savdolar = Savdo.objects.filter(sana__range=[start_date, end_date])
            chiqimlar = Chiqim.objects.filter(sana__range=[start_date, end_date])

            # jami chiqim
            chiqimlar_summa = chiqimlar.values_list('summa', flat=True)
            jami_chiqim = sum(chiqimlar_summa)

            # jami savdo
            savdolar_summa = savdolar.values_list('summa', flat=True)
            jami_savdo = sum(savdolar_summa)

            # savdo qilingan barcha mahsulotlar tannarxi
            savdolar_mahsulot = savdolar.values_list('mahsulot', flat=True)
            savdolar_miqdor = savdolar.values_list('miqdor', flat=True)
            savdo_mahsulot = 0
            for i in range(len(savdolar_mahsulot)):
                savdo_mahsulot += (Mahsulot.objects.get(id=savdolar_mahsulot[i]).narx1 * savdolar_miqdor[i])

            # mijozlar_soni
            savdolar_mijoz = savdolar.values_list('mijoz', flat=True)
            kelgan_mijozlar = set(savdolar_mijoz)
            mijozlar_soni = len(set(savdolar_mijoz))
            print(savdolar_mijoz)

            # foyda
            sotuvdan_foyda = jami_savdo - savdo_mahsulot
            jami_foyda = jami_savdo - jami_chiqim

            return Response({
                'jami_foyda': jami_foyda,
                'sotuvdan_foyda': sotuvdan_foyda,
                'jami_chiqim': jami_chiqim,
                'jami_savdo_qiymati': jami_savdo,
                'sotilgan_mahsulotlar_tannarxi': savdo_mahsulot,
                'mijozlar_soni': mijozlar_soni,
                'mijozlar': kelgan_mijozlar
            })
        except Exception:
            return Response({
                "success": False,
                "message": "Timedelta kiritishda xatolik!"
            })


class StatsSavdolarAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="start_date",
                in_=openapi.IN_QUERY,
                description="Boshlang'ich sanaga (YYYY-MM-DD) ko'ra savdolarni filtrlash",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
            openapi.Parameter(
                name="end_date",
                in_=openapi.IN_QUERY,
                description="Oxirgi sanaga (YYYY-MM-DD) ko'ra savdolarni filtrlash",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
        ],
    )
    def get(self, request):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            savdolar = Savdo.objects.filter(sana__range=[start_date, end_date])
            serializer = SavdoSerializer(savdolar, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({
                "success": False,
                "message": "Noto'g'ri sana formati kiritildi. Sana formati 'YYYY-MM-DD' bo'lishi kerak."
            })


class StatsChiqimlarAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="start_date",
                in_=openapi.IN_QUERY,
                description="Boshlang'ich sanaga (YYYY-MM-DD) ko'ra chiqimlarni filtrlash",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
            openapi.Parameter(
                name="end_date",
                in_=openapi.IN_QUERY,
                description="Oxirgi sanaga (YYYY-MM-DD) ko'ra chiqimlarni filtrlash",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
        ],
    )
    def get(self, request):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            chiqimlar = Chiqim.objects.filter(sana__range=(start_date, end_date))
            serializer = ChiqimSerializer(chiqimlar, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({
                "success": False,
                "message": "Noto'g'ri sana formati kiritildi. Sana formati 'YYYY-MM-DD' bo'lishi kerak."
            })


class StatsMijozlarAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="start_date",
                in_=openapi.IN_QUERY,
                description="Boshlang'ich sanaga (YYYY-MM-DD) ko'ra chiqimlarni filtrlash",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
            openapi.Parameter(
                name="end_date",
                in_=openapi.IN_QUERY,
                description="Oxirgi sanaga (YYYY-MM-DD) ko'ra chiqimlarni filtrlash",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
        ],
    )
    def get(self, request):
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            mijozlar = Mijoz.objects.filter(savdolar__sana__range=(start_date, end_date)).distinct()
            serializer = MijozSerializer(mijozlar, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({
                "success": False,
                "message": "Noto'g'ri sana formati kiritildi. Sana formati 'YYYY-MM-DD' bo'lishi kerak."
            })























