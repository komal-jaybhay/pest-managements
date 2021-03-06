import sys
import traceback
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from api.models import Transactions, TransactionMedia, Question, QuestionTransactions, QuestionTransactionMedia
from api.whatsapp_api import get_item_text, get_message, send_message, validate_twilio_request, getmediafiles, storemediafiles
from insect.object_detection import get_insects
from logger.logger import Logger
from datetime import datetime



log = Logger('API')
# Create your views here.

def create_transaction(request, incoming_msg, trans_from, noofmedia):
    """Create a log."""
    # import pdb;pdb.set_trace()
    media_obj = []
    try:
        trans_obj = Transactions(trans_type='whatsapp', trans_from=trans_from, trans_msg=incoming_msg)
        trans_obj.save()
        if int(noofmedia)>0:
            stored_files = storemediafiles(request, noofmedia)
            for each in stored_files:
                trans_media_obj = TransactionMedia(transation_fk=trans_obj)
                trans_media_obj.save()
                trans_media_obj.trans_media.save("%s" % each[1], File(each[0]))
                trans_media_obj.save()
                media_obj.append(trans_media_obj)
    except Exception as e:
        log_error(e)
    return media_obj


@require_POST
@csrf_exempt
@validate_twilio_request
def incoming_message(request):
    # import pdb;pdb.set_trace()
    log.set_logger("Info - Message Received. Message Details {}".format(request.POST))
    try:
        incoming_msg = request.POST['Body'] #request.values.get('Body', '').lower()
        msg_from = request.POST['From'] #request.values.get('From', '')
        msg_to = request.POST['To'] #request.values.get('To', '')
        noofmedia = request.POST['NumMedia']
        from_number = msg_from.split('whatsapp:')[1]
        # incoming_msg, work_type = get_item_text(incoming_msg)
        if incoming_msg.strip() in ['', None] and noofmedia == 0:
            send_message(request, "We didn't find any image.", msg_to, msg_from)
            return HttpResponse('Message Sent!', 200)

        incoming_msg = incoming_msg.strip()
        trans_objs = create_transaction(request, incoming_msg, from_number, noofmedia)
        # import pdb;
        # pdb.set_trace()
        if not trans_objs == []:
            for each_obj in trans_objs:
                each_url = ''.join([settings.WEBHOST_URL, each_obj.trans_media.url])
                uuid = each_obj.transation_fk.trans_uid
                insects, label = get_insects(each_url, settings.MEDIA_ROOT, from_number, uuid)
                # import pdb;
                # pdb.set_trace()
                if insects == "":
                    send_message(request, "Didn't find any insect", msg_to, msg_from, each_url)
                else:
                    insect_control_dict = {
                        'aphid':'Aphids suck plant sap, causing foliage to distort and leaves to drop; honeydew excreted on leaves supports sooty mold growth; and feeding spreads viral diseases.\n\nControl these bugs:\n\nWash plants with strong spray of water \nEncourage native predators and parasites such as aphid midges, lacewings, and lady beetles \nWhen feasible, cover plants with floating row covers \nApply hot-pepper or garlic repellent sprays \n',
                        'caterpillar':'Caterpillars are soft, segmented larvae with distinct, harder head capsule with six legs in the front and fleshy false legs on rear segments. They can be found on many fruits and vegetables, ornamentals, and shade trees. Caterpillars chew on leaves or along margins; some tunnel into fruits. \n\nTo deter them:\n\nEncourage native predators and parasites\nHand-pick your harvest\n',
                        'flea beetle':'Flea beetles are small, dark beetles that jump like fleas when disturbed. They hang out on most vegetable crops and are found throughout North America. Adults chew numerous small, round holes into leaves (most damaging to young plants), and larvae feed on plant roots.\n\nFor control:\n\nApply floating row covers\nSpray plants with garlic spray or kaolin clay\n',
                        }
                    # full_message = '\n\n'.join(
                    #     [labels.title(), 'Advisory: This is sample advisory.', 'Suggestion: This is sample suggestion.'])
                    full_message = ''
                    for each_label in label:
                        try:
                            each_message = '\n\n'.join(
                                [each_label.title(), insect_control_dict[each_label]])
                        except:
                            each_message = '\n'.join(
                                [each_label.title(), 'Details not filled.'])
                        full_message = ''.join(
                                [full_message, each_message, '------------------------------------\n'])
                    print(each_url)
                    send_message(request, full_message, msg_to, msg_from, each_url)
                print(each_obj.trans_media)
                print(each_obj.transation_fk.trans_uid)

        # res = getmediafiles(request, noofmedia)
        # image_labels = []
        # if not res == []:
        #     for each_url in res:
        #         each_label = []
        #         labels = get_insects(each_url)
        #         if labels == "":
        #             send_message(request, "Didn't find any insect", msg_to, msg_from, each_url)
        #         else:
        #             send_message(request, "labels", msg_to, msg_from, each_url)
        #         # each_label.append(each_url)
        #         # str_label = ', '.join(labels)
        #         # each_label.append(str_label)
        #         # image_labels.append(each_label)
        #     # for each_img in image_labels:
        #     #     message =
        #     #     send_message(request, "Didn't find any image", msg_to, msg_from)
        else:
            send_message(request, "Didn't find any image", msg_to, msg_from)

        # Return the TwiML
    except Exception as e:
        log_error(e)
    return HttpResponse('Message Sent!', 200)


def get_seq_message(request, incoming_msg, trans_from):
    """Create a log."""
    # import pdb;pdb.set_trace()
    try:
        query_date = datetime.now()
        trans_obj = QuestionTransactions.object.filter(trans_type='whatsapp', trans_from=trans_from, trans_date=query_date).order_by('-id')[:1]
        if trans_obj:
            print(trans_obj.question_fk)
            obj = Question.object.filter(id=trans_obj.question_fk)
            query_obj = Question.object.filter(sequence=obj.sequence+1)

        else:
            query_obj = Question.object.filter().order_by('sequence')[:1]
        return query_obj.question

    except Exception as e:
        log_error(e)
        return False


@require_POST
@csrf_exempt
@validate_twilio_request
def incoming_Q_message(request):
    # import pdb;pdb.set_trace()
    log.set_logger("Info - Message Received. Message Details {}".format(request.POST))
    try:
        incoming_msg = request.POST['Body'] #request.values.get('Body', '').lower()
        msg_from = request.POST['From'] #request.values.get('From', '')
        msg_to = request.POST['To'] #request.values.get('To', '')
        noofmedia = request.POST['NumMedia']
        from_number = msg_from.split('whatsapp:')[1]
        # incoming_msg, work_type = get_item_text(incoming_msg)
        if incoming_msg.strip() in ['', None] and noofmedia == 0:
            send_message(request, "We didn't find any image.", msg_to, msg_from)
            return HttpResponse('Message Sent!', 200)

        incoming_msg = incoming_msg.strip()
        trans_objs = create_transaction(request, incoming_msg, from_number, noofmedia)
        # import pdb;
        # pdb.set_trace()
        if not trans_objs == []:
            for each_obj in trans_objs:
                each_url = ''.join([settings.WEBHOST_URL, each_obj.trans_media.url])
                uuid = each_obj.transation_fk.trans_uid
                labels = get_insects(each_url, settings.MEDIA_ROOT, from_number, uuid)
                print(each_url)
                # import pdb;
                # pdb.set_trace()
                if labels == "":
                    send_message(request, "Didn't find any insect", msg_to, msg_from, each_url)
                else:
                    send_message(request, labels, msg_to, msg_from, each_url)
                print(each_obj.trans_media)
                print(each_obj.transation_fk.trans_uid)

        # res = getmediafiles(request, noofmedia)
        # image_labels = []
        # if not res == []:
        #     for each_url in res:
        #         each_label = []
        #         labels = get_insects(each_url)
        #         if labels == "":
        #             send_message(request, "Didn't find any insect", msg_to, msg_from, each_url)
        #         else:
        #             send_message(request, "labels", msg_to, msg_from, each_url)
        #         # each_label.append(each_url)
        #         # str_label = ', '.join(labels)
        #         # each_label.append(str_label)
        #         # image_labels.append(each_label)
        #     # for each_img in image_labels:
        #     #     message =
        #     #     send_message(request, "Didn't find any image", msg_to, msg_from)
        else:
            send_message(request, "Didn't find any image", msg_to, msg_from)

        # Return the TwiML
    except Exception as e:
        log_error(e)
    return HttpResponse('Message Sent!', 200)

def log_error(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_in = repr(traceback.format_tb(exc_traceback)[-1])
    message = ' - '.join(['Error', str(e), error_in])
    log.set_logger(message)