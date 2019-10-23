# Install

    git clone https://github.com/shemigon/drf-app.git
    cd drf-app
    # python 3.6 or 3.7 is best
    ./reset.sh python3.7
    env/bin/python ./manage.py runserver

# Default data

Admin:

- email: root@localhost
- password: 123

Organizations:

* Organization 1 (@org1.com)
* Organization 2 (@org2.com)

Every organization has users with the same password **user**:
    
* admin@orgN.com
* viewer@orgN.com
* user@orgN.com

For example, to login as an admin in Organization 1, use _admin@org1.com_ / _user_.
