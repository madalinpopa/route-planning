# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Export environment variables
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

export FLASK_APP := "route_planning"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Custom Flask commands
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

create-user username email password:
    flask user create {{ username }} {{ email }} {{ password }}

delete-user username:
    flask user delete {{ username }}

list-users:
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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Dev commands
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

run:
    flask run --debug

tailwindcss:
    npm run tailwindcss-watch

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Translation commands
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

translate:
    pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .

init-lang lang=ro:
    pybabel init -i messages.pot -d translations -l {{ lang }}

compile-lang:
    pybabel compile -d translations

update-lang:
    pybabel update -i messages.pot -d translations