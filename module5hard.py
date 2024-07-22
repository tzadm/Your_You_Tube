class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = hash(password)
        self.age = age

    def __eq__(self, other):
        return self.nickname == other.nickname and self.password == other.password and self.age == other.age

    def __hash__(self):
        return hash((self.nickname, self.password, self.age))

    def __str__(self):
        return f'{self.nickname}, {self.password},{self.age}'


class Video:

    def __init__(self, title, duration, time_now=0, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode


class UrTube:
    users = []
    videos = []
    current_user = None
    g = 0

    def __contains__(self, title):
        return any(title == obj.title for obj in self.videos)

    def log_in(self, nickname, password):
        modified_adult_mode = []
        nickname_passwords_hash = []
        user_hash = nickname, hash(password)
        user_hash = hash(user_hash)
        for i in self.users:
            hash_2 = i.nickname, i.password
            nickname_passwords_hash.append(hash(hash_2))
        dickt_ = dict(zip(nickname_passwords_hash, self.users))

        if user_hash in dickt_.keys():
            self.current_user = dickt_[user_hash].nickname

            if dickt_[user_hash].age < 18:
                for i in self.videos:
                    i.adult_mode = True
                    modified_adult_mode.append(i)
                self.videos = modified_adult_mode

            if dickt_[user_hash].age > 18:
                for i in self.videos:
                    i.adult_mode = False
                    modified_adult_mode.append(i)
                self.videos = modified_adult_mode
        else:
            for i in self.videos:
                i.adult_mode = False
                modified_adult_mode.append(i)
            self.videos = modified_adult_mode
            self.log_out()
            print('\nНеправильные учетные данные!')

    def register(self, nickname, password, age):
        users1 = []
        self.g += 1
        x = globals()
        x[f'user{self.g}'] = User(nickname, password, age)
        for i in self.users:
            users1.append(i.nickname)
        if nickname in users1:
            print(f'Пользователь {nickname} уже существует')
        if nickname not in users1:
            self.users.append(x[f'user{self.g}'])
            self.log_in(nickname, password)

    def log_out(self):
        self.current_user = None

    def add(self, *args):
        videos_ = []
        for i in self.videos:
            videos_.append(i.title)
        for q in args:
            if q.title not in videos_:
                self.videos.append(q)

    def get_videos(self, word):
        get_videos = []
        title_videos = []
        for i in self.videos:
            title_videos.append(i.title)
        for q in title_videos:
            q = str(q)
            if word.lower() in q.lower():
                get_videos.append(q)
        return get_videos

    def watch_video(self, movie_title):
        import time
        adult_mode_use = ''
        duration_use = ''
        time_now_use = ''

        for i in self.videos:
            if movie_title == i.title:
                adult_mode_use = i.adult_mode
                duration_use = i.duration
                time_now_use = i.time_now

        if movie_title in UrTube():
            if self.current_user is None:
                print('Войдите в аккаунт, чтобы смотреть видео')
            elif adult_mode_use:
                print('Вам нет 18 лет, пожалуйста покиньте страницу')
            else:
                for i in range(duration_use):
                    time.sleep(1)
                    time_now_use += 1
                    print(1 + i, end=' ', )
                print('Конец фильма')

            # elif time_now_use == 0:
            #     for i in range(duration_use):
            #         time.sleep(1)
            #         print(1 + i, end=' ', )
            #     print('Конец фильма')
            # else:
            #     duration_use = time_now_use
            #     for i in range(duration_use):
            #         time.sleep(1)
            #         print(1 + i, end=' ', )
            #     print('Конец фильма')


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
