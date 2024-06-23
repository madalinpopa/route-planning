

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Flask Migration
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
db-init:
    flask --app route_planning db init

db-migrate:
    flask --app route_planning db migrate

db-upgrade:
    flask --app route_planning db upgrade