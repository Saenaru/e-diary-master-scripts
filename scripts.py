import random
from datacenter.models import Mark, Chastisement, Lesson, Schoolkid


COMMENDATION_TEXTS = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!"
]


def get_schoolkid(schoolkid_name):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем '{schoolkid_name}' не найден.")
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем '{schoolkid_name}'. Уточните запрос.")
    return None


def fix_marks(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    if not schoolkid:
        return

    marks_to_update = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    updated_count = marks_to_update.update(points=5)

    if updated_count > 0:
        print(f"Оценки успешно исправлены для {schoolkid.full_name}. Оценок исправлено: {updated_count}.")
    else:
        print(f"Нет оценок, требующих исправления для {schoolkid.full_name}.")


def remove_chastisements(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    if not schoolkid:
        return

    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements_count = chastisements.count()
    chastisements.delete()
    
    print(f"Удалено замечаний: {chastisements_count} для ученика {schoolkid.full_name}.")


def create_commendation(schoolkid_name, subject_title):
    schoolkid = get_schoolkid(schoolkid_name)
    if not schoolkid:
        return

    commendation_text = random.choice(COMMENDATION_TEXTS)

    last_lesson = Lesson.objects.filter(
        subject__title=subject_title,
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter
    ).order_by('-date').first()

    if not last_lesson:
        print(f"Уроки по предмету '{subject_title}' не найдены для '{schoolkid_name}'.")
        return

    Commendation.objects.create(
        text=commendation_text,
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
    )

    print(f"Похвала успешно создана для {schoolkid.full_name} на дату {last_lesson.date}.")