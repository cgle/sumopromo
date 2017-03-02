from sqlalchemy.dialects.postgresql import ENUM

# DAYS OF WEEK
#
days_of_week = ('sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',)
days_of_week_enum = ENUM(*days_of_week, name='day_of_week')

# BUSINESS TYPE
#
business_types = ('regular_business', 'sumo_business',)
business_types_enum = ENUM(*business_types, name='business_type')
