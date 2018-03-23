import React, { Component } from 'react';
import './Users.css';
import {Form, FormGroup, ControlLabel, FormControl, FieldGroup, Button} from 'react-bootstrap'
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table'


var products = []
for (var i = 0; i < 100; i++) {
    var newprod = {
        name: "Brian" + i,
        role: "Scrum Master",
        email: "fake@fake.com",
        lastlogin: "now"
    };
    products.push(newprod);
}
function onDeleteRow(rowKeys) {
    alert('You deleted: ' + rowKeys)
/*   const data = new FormData(event.target);
    fetch('/api/form-submit-url', {
        method: 'POST',
        body: data,
    });*/
}

const options = {
    afterDeleteRow: onDeleteRow
}

var selectRowProp = {
    mode: "checkbox",
    clickToSelect: true,
};


class Users extends Component {
    constructor(props, context) {
        super(props, context);

        this.handleChange = this.handleChange.bind(this);

        this.state = {
            name: '',
            password: '',
            passwordverify: '',
            email:'',
            role:''
        };
    }

    getValidationState() {
        const length = this.state.password.length;
        if (length > 10) return 'success';
        else if (length > 5) return 'warning';
        else if (length > 0) return 'error';
        return null;
    }
    getVerifyPassword(){
        if(this.state.passwordverify==='') return null;
        if(this.state.password === this.state.passwordverify) return 'success';
        else return 'error';
        return null;
    }


    handleChange(e) {
        this.setState({ [e.target.id]: e.target.value});
    }

    render() {
        return (
            <div className="container">
            <form className="form-createuser">
                <FormGroup
                    className="name-input"
                    controlId="name"
                >
                    <ControlLabel>User Name</ControlLabel>

                    <FormControl
                        type="text"
                        value={this.state.name}
                        placeholder="Enter User Name"
                        onChange={this.handleChange}
                    />
                    <FormControl.Feedback />
                </FormGroup>
                <FormGroup
                    className="email-input"
                    controlId="email"
                >
                    <ControlLabel>Email</ControlLabel>

                    <FormControl
                        type="text"
                        value={this.state.email}
                        placeholder="Enter email"
                        onChange={this.handleChange}
                    />
                    <FormControl.Feedback />
                </FormGroup>

                <FormGroup
                    className="pass-input"
                    controlId="password"
                    validationState={this.getValidationState()}
                 >
                    <ControlLabel>Password</ControlLabel>
                    <FormControl
                        type="password"
                        value={this.state.password}
                        placeholder="Enter password"
                        onChange={this.handleChange}
                    />
                    <FormControl.Feedback />
                </FormGroup>
                <FormGroup
                    className={"pass-verify-input"}
                    controlId="passwordverify"
                    validationState={this.getVerifyPassword()}
                >
                    <ControlLabel>Verify Password</ControlLabel>

                    <FormControl
                        type="password"
                        value={this.state.passwordverify}
                        placeholder="Re-Enter password"
                        onChange={this.handleChange}
                    />
                    <FormControl.Feedback />
                </FormGroup>
                <FormGroup
                    className="role-input"
                    controlId="role"
                >
                    <ControlLabel></ControlLabel>
                    <FormControl componentClass="select" placeholder="select" onChange={this.handleChange}>

                        <option value="admin">Admin</option>
                        <option value="operator">Operator</option>

                    </FormControl>
                </FormGroup>
                <Button className="button-submit" type="submit">Create User</Button>
            </form>
            <BootstrapTable className="table-user" data={products} selectRow={selectRowProp} options={options}   striped={true} hover={true} deleteRow pagination>
               <TableHeaderColumn dataField="name" isKey={true}  width="150"  dataSort>User Name</TableHeaderColumn>
               <TableHeaderColumn dataField="role"  width="150" >Role</TableHeaderColumn>
               <TableHeaderColumn dataField="email"  width="200" >Email</TableHeaderColumn>
               <TableHeaderColumn dataField="lastlogin"  width="150" dataSort >last Login</TableHeaderColumn>
            </BootstrapTable>
            </div>
        );
    }
}

export default Users;