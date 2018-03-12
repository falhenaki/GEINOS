/*** @jsx React.DOM */



/*const obj = [{
  name: "onion",
  price: ".99",
  id: 1
}, {
  name: "pepper",
  price: "1.25",
  id: 2
}, {
  name: "broccoli",
  price: "3.00",
  id: 3
}];

class TableRow extends React.Component {
  render() {
    const {
      data
    } = this.props;
    const row = data.map((data) =>
    <tr>
      <td key={data.name}>{data.name}</td>
      <td key={data.id}>{data.id}</td>
      <td key={data.price}>{data.price}</td>
    </tr>
    );
    return (
      <span>{row}</span>
    );
  }
}

class Table extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <table>
        <TableRow data={this.props.data} />
      </table>
    );
  }
}*/
// products will be presented by react-bootstrap-table
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
      <TableHeaderColumn dataField="email" width="350" >Email</TableHeaderColumn>
      <TableHeaderColumn dataField="lastlogin" width="150" dataSort={true} >Last Login</TableHeaderColumn>
  </BootstrapTable>,
    document.getElementById("userTable")
);
//ReactDOM.render(<Table/>, document.getElementById("userTable"));