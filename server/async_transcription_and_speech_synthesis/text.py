from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from async_transcription_and_speech_synthesis.models import DataRecognitionAndSynthesis, Text
from async_transcription_and_speech_synthesis.serializers import TextSerializer

# Пагинация
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def text(request):
    # Получаем список текстов
    texts = Text.objects.all()

    # кол-во услуг на странице
    count_item = request.GET.get('count_item', 5)
    # Пагинации
    paginator = PageNumberPagination()
    # Количество элементов на странице
    paginator.page_size = count_item
    # Параметр запроса для изменения количества элементов на странице
    paginator.page_size_query_param = 'page_size'
    # Максимальное количество элементов на странице
    paginator.max_page_size = count_item

    result_page = paginator.paginate_queryset(texts, request)
    texts_serializer = TextSerializer(result_page, many=True)

    return Response(
        data={
            'count': paginator.page.paginator.count,
            'data': texts_serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def text_by_pk(request, pk):
    try:
        data = DataRecognitionAndSynthesis.objects.get(pk=pk)
        text = data.text
        serializer = TextSerializer(text)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except DataRecognitionAndSynthesis.DoesNotExist:
        return Response({'error': 'Текст не найден'}, status=status.HTTP_404_NOT_FOUND)
