# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Export environment variables
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

export FLASK_APP := "route_planning"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Custom Flask commands
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

create_user username email password:
    flask user create {{ username }} {{ email }} {{ password }}

delete_user username:
    flask user delete {{ username }}

list_users:
    flask user list

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Flask Migration
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

db-init:
    flask db init

db-migrate:
    flask db migrate

db-upgrade:
    flask db upgrade