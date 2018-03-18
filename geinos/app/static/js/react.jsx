/*** @jsx React.DOM */

var products = []
for (var i = 0; i < data.length; i++) {
          var newprod = {
        name: data[i][0],
        role: data[i][1],
        email: "test@test",
        lastlogin: "2 hours ago"
      };
      products.push(newprod);
}

var products_1 = []
for (var i = 0; i < data.length; i++) {
          var newprod = {
        name: data[i][0],
        role: data[i][1],
        email: "test@test",
        lastlogin: "2 hours ago"
      };
      products_1.push(newprod);
}

    React.render(
        <BootstrapTable data={products} striped={true} hover={true}>
            <TableHeaderColumn dataField="name" width="250" isKey={true} dataAlign="center"
                               dataSort={true}>User</TableHeaderColumn>
            <TableHeaderColumn dataField="role" width="150">Role</TableHeaderColumn>
            <TableHeaderColumn dataField="email" width="250">Email</TableHeaderColumn>
            <TableHeaderColumn dataField="lastlogin" width="150" dataSort={true}>Last Login</TableHeaderColumn>
        </BootstrapTable>,
        document.getElementById("userTable")
    );

    React.render(
        <BootstrapTable data={products_1} striped={true} hover={true}>
            <TableHeaderColumn dataField="name" width="250" isKey={true} dataAlign="center"
                               dataSort={true}>User</TableHeaderColumn>
            <TableHeaderColumn dataField="role" width="150">Role</TableHeaderColumn>
            <TableHeaderColumn dataField="email" width="250">Email</TableHeaderColumn>
            <TableHeaderColumn dataField="lastlogin" width="150" dataSort={true}>Last Login</TableHeaderColumn>
        </BootstrapTable>,
        document.getElementById("LogTable")
    );