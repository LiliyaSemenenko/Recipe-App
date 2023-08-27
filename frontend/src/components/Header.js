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
                            <Navbar.Brand href="#">Recipes For Everyone</Navbar.Brand>
                        </LinkContainer>

                        <Navbar.Toggle aria-controls="navbarScroll" />
                        <Navbar.Collapse id="navbarScroll">

                            {/* <SearchBox /> */}
                            <Nav className="ml-auto">

                                    <NavDropdown title="Recipes" id="RecipesScrollingDropdown">
                                        <NavDropdown.Item href="/breakfast">Breakfast</NavDropdown.Item>
                                        <NavDropdown.Item href="/lunch">Lunch</NavDropdown.Item>
                                        <NavDropdown.Item href="/dinner">Dinner</NavDropdown.Item>
                                        <NavDropdown.Item href="/drinks">Drinks</NavDropdown.Item>
                                        <NavDropdown.Item href="/desserts">Desserts</NavDropdown.Item>
                                    </NavDropdown>

                                <Nav.Link href="/ingredients">Ingredients</Nav.Link>
                                <Nav.Link href="/trends">Trends</Nav.Link>
                            </Nav>
                            <Nav className="ms-auto">
                                <Nav.Link href="/post">Post</Nav.Link>
                                <Nav.Link href="/login"><i className="fas fa-user"></i>Login</Nav.Link>

                            </Nav>

                        </Navbar.Collapse>
                    </Container>
                </Navbar>
            </header>
        </div>
    )
}

export default Header

//                             <Nav
//                                 className="me-auto my-2 my-lg-0"
//                                 style={{ maxHeight: '100px' }}
//                                 navbarScroll
//                             >
//                                 <Nav.Link href="/recipes">Recipes</Nav.Link>
//                                 <Nav.Link href="/ingredients">Ingredients</Nav.Link>
//                                 <Nav.Link href="/trends">Trends</Nav.Link>
//                                 <Nav.Link href="/post">Post</Nav.Link>
//                                 <Nav.Link href="/login"><i className="fas fa-user"></i>Login</Nav.Link>

//                                 <NavDropdown title="Recipes" id="RecipesScrollingDropdown">
//                                     <NavDropdown.Item href="/breakfast">Breakfast</NavDropdown.Item>
//                                     <NavDropdown.Item href="/lunch">Lunch</NavDropdown.Item>
//                                     <NavDropdown.Item href="/dinner">Dinner</NavDropdown.Item>
//                                     <NavDropdown.Item href="/drinks">Drinks</NavDropdown.Item>
//                                     <NavDropdown.Item href="/desserts">Desserts</NavDropdown.Item>
//                                     <NavDropdown.Item href="/veg">Vegiterian and Vegan</NavDropdown.Item>

//                                     <NavDropdown.Divider />
//                                     <NavDropdown.Item href="#action9">
//                                         Something else here
//                                     </NavDropdown.Item>
//                                 </NavDropdown>
//                                 <Nav.Link href="#" disabled>
//                                     Link
//                                 </Nav.Link>
//                             </Nav>
//                         <Form className="d-flex">
//                             <Form.Control
//                             type="search"
//                             placeholder="Search"
//                             className="me-2"
//                             aria-label="Search"
//                             />
//                             <Button variant="outline-success">Search for a recipe</Button>
//                         </Form>
//                         </Navbar.Collapse>
//                     </Container>
//                 </Navbar>
//             </header>
//         </div>
//     )
// }

// export default Header