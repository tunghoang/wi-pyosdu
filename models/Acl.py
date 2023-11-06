class Acl:
  viewers = ['data.default.viewers@osdu.group']
  owners = ['data.default.owners@osdu.group']

  def __init__(self, viewers = [], owners = []):
    self.viewers = self.viewers + viewers
    self.owners = self.owners + owners
