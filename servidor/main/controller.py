from servidor.common.controllers import SuperController
from servidor.common.utils import decorators
from tornado.web import authenticated
from tornado.gen import coroutine

class Index(SuperController):

    @decorators(authenticated, coroutine)
    def get(self):
        try:
            usuario = self.get_user()

            if usuario:
                self.render("main/index.html", user=usuario)
            else:
                self.redirect('/logout')
        except Exception as e:
            print(e)
            self.redirect('/logout')
