
# Основные классы системы управления заявками

class RequestStatisticsFixed:
    """Класс для расчета статистики по заявкам."""

    def __init__(self, requests_data):
        self.requests_data = requests_data.copy()
        self.completed_status = 'Готова к выдаче'

    def calculate_completed_count(self):
        """Рассчитывает количество выполненных заявок."""
        if 'requestStatus' not in self.requests_data.columns:
            return 0
        completed_mask = self.requests_data['requestStatus'].fillna('') == self.completed_status
        return self.requests_data[completed_mask].shape[0]

    def calculate_average_duration(self):
        """Рассчитывает среднее время выполнения заявок."""
        if 'duration_days' not in self.requests_data.columns:
            return None
        duration_values = pd.to_numeric(self.requests_data['duration_days'], errors='coerce')
        valid_durations = duration_values.dropna()
        return round(valid_durations.mean(), 2) if len(valid_durations) > 0 else None

class RequestManagementSystem:
    """Класс для управления системой заявок на ремонт."""

    def __init__(self, requests_data, users_data, comments_data):
        self.requests_data = requests_data
        self.users_data = users_data
        self.comments_data = comments_data
        self.current_user = None

    def authenticate_user(self, login, password):
        """Аутентификация пользователя."""
        try:
            user_mask = ((self.users_data['login'] == login) & 
                        (self.users_data['password'] == password))
            if user_mask.any():
                user_info = self.users_data[user_mask].iloc[0]
                self.current_user = {
                    'userID': user_info['userID'],
                    'fio': user_info['fio'],
                    'type': user_info.get('type', 'Неизвестно')
                }
                return True
            return False
        except Exception:
            return False
        