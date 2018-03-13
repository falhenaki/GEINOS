/*** @jsx React.DOM */
var products = [{
      name: "Brian",
      role: "Admin",
      email: "brian@brian.com",
      lastlogin:"2 hours ago"
  },{
      name: "Steve",
      role: "Operator",
      email: "steve@steve.com",
      lastlogin:"3 hours ago"
  }];

React.render(
  <BootstrapTable data={products} striped={true} hover={true}>
      <TableHeaderColumn dataField="name" width="250" isKey={true} dataAlign="center" dataSort={true}>User</TableHeaderColumn>
      <TableHeaderColumn dataField="role" width="150" >Role</TableHeaderColumn>
      <TableHeaderColumn dataField="email" width="250" >Email</TableHeaderColumn>
      <TableHeaderColumn dataField="lastlogin" width="150" dataSort={true} >Last Login</TableHeaderColumn>
  </BootstrapTable>,
    document.getElementById("userTable")
);
