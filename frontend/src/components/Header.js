import React from 'react'
import { Button, Form, Navbar, Nav, Container, Row , NavDropdown} from 'react-bootstrap'
// import { useDispatch, useSelector } from 'react-redux'
import { LinkContainer } from 'react-router-bootstrap'
// import SearchBox from './SearchBox'
// import { logout } from '../actions/userActions'


function Header() {

    return (
        <div>
            <header>
                <Navbar bg="dark" variant="light" expand="lg" className="bg-body-tertiary" CollapseOnSelect>
                    <Container fluid>
                        <LinkContainer to='/'>
                            <Navbar.Brand>Recipes For Everyone</Navbar.Brand>
                        </LinkContainer>

                        <Navbar.Toggle aria-controls="navbarScroll" />
                        <Navbar.Collapse id="navbarScroll">

                            {/* <SearchBox /> */}

                            <Nav className="ml-auto">

                                <LinkContainer to='/recipes'>
                                    <NavDropdown title="Recipes" id="RecipesScrollingDropdown">
                                        <LinkContainer to='/recipes/breakfast'>
                                            <NavDropdown.Item>Breakfast</NavDropdown.Item>
                                        </LinkContainer>
                                        <LinkContainer to='/recipes/lunch'>
                                            <NavDropdown.Item>Lunch</NavDropdown.Item>
                                        </LinkContainer>
                                        <LinkContainer to='/recipes/dinner'>
                                            <NavDropdown.Item>Dinner</NavDropdown.Item>
                                        </LinkContainer>
                                        <LinkContainer to='/recipes/drinks'>
                                            <NavDropdown.Item>Drinks</NavDropdown.Item>
                                        </LinkContainer>
                                        <LinkContainer to='/recipes/desserts'>
                                            <NavDropdown.Item>Desserts</NavDropdown.Item>
                                        </LinkContainer>
                                    </NavDropdown>
                                </LinkContainer>

                            </Nav>

                            <Nav className="ms-auto">
                                <LinkContainer to='/post'>
                                    <Nav.Link>POST</Nav.Link>
                                </LinkContainer>

                                <LinkContainer to='/login'>
                                    <Nav.Link><i className="fas fa-user"></i>Login</Nav.Link>
                                </LinkContainer>
                            </Nav>

                        </Navbar.Collapse>
                    </Container>
                </Navbar>
            </header>
        </div>
    )
}

export default Header
