import React, { useState, useEffect } from 'react'
// import { useDispatch, useSelector } from 'react-redux'
import { Link, useParams  } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card, Form } from 'react-bootstrap'
import Rating from '../components/Rating'
import recipes from '../recipes'
// import Loader from '../components/Loader'
// import Message from '../components/Message'
// import { listProductDetails, createProductReview } from '../actions/recipeActions'
// import { PRODUCT_CREATE_REVIEW_RESET } from '../constants/recipeConstants'

function RecipeScreen({ match }) {
    // const recipe = recipes.find((p) => p._id == match.params.id)
    const { id } = useParams();
    const recipe = recipes.find((p) => p._id === id);

    return(
        <div>

            <Button as={Link} to="/">Go Back</Button>

            <Row style={{ marginTop: '20px' }} className="justify-content-center">
                <Col md={5}>
                    <Image src={recipe.image} alt={recipe.name} fluid />
                </Col>

                <Col md={3}>
                    <ListGroup variant="flush">
                        <ListGroup.Item>
                            <h3>{recipe.name}</h3>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <Rating value={recipe.rating} text={`${recipe.numComments} comments`} color={'#f8e825'} />
                        </ListGroup.Item>

                        <ListGroup.Item>
                            Price: ${recipe.price}
                        </ListGroup.Item>

                        <ListGroup.Item>
                            Description: {recipe.description}
                        </ListGroup.Item>
                    </ListGroup>

                    <br></br>

                    <Col md={10}>
                        <Card>
                            <ListGroup variant='flush'>
                                <ListGroup.Item>
                                    <Row>
                                        <Col>Price:</Col>
                                        <Col>
                                            <strong>${recipe.price}</strong>
                                        </Col>
                                    </Row>
                                </ListGroup.Item>
                                <ListGroup.Item>
                                    <Row>
                                        <Col>Status:</Col>
                                        <Col>
                                            {recipe.countInStock > 0 ? 'In Stock' : 'Out of Stock'}
                                        </Col>
                                    </Row>
                                </ListGroup.Item>

                                {recipe.countInStock > 0 && (
                                    <ListGroup.Item>
                                        <Row>
                                            <Col>Qty</Col>
                                            <Col xs='auto' className='my-1'>
                                                <Form.Control
                                                    as="select"
                                                    // value={qty}
                                                    // onChange={(e) => setQty(e.target.value)}
                                                >
                                                    {

                                                        [...Array(recipe.countInStock).keys()].map((x) => (
                                                            <option key={x + 1} value={x + 1}>
                                                                {x + 1}
                                                            </option>
                                                        ))
                                                    }

                                                </Form.Control>
                                            </Col>
                                        </Row>
                                    </ListGroup.Item>
                                )}


                                <ListGroup.Item>
                                    <Button
                                        // onClick={addToCartHandler}
                                        className='btn-block'
                                        disabled={recipe.countInStock == 0}
                                        type='button'>
                                        Add to Cart
                                    </Button>
                                </ListGroup.Item>
                            </ListGroup>
                        </Card>
                    </Col>
                </Col>
            </Row>

        </div>
    )
}

export default RecipeScreen