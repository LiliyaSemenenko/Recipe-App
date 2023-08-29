import React, { useState, useEffect } from 'react'
import axios from 'axios'
// import { useDispatch, useSelector } from 'react-redux'
import { Link, useParams  } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card, Form } from 'react-bootstrap'
import Rating from '../components/Rating'
// import recipes from '../recipes'
// import Loader from '../components/Loader'
// import Message from '../components/Message'
// import { listProductDetails, createProductReview } from '../actions/recipeActions'
// import { PRODUCT_CREATE_REVIEW_RESET } from '../constants/recipeConstants'

function RecipeScreen({ match }) {

    const { id } = useParams();
    const [recipe, setRecipe] = useState([])

    useEffect(() => {
        async function fetchRecipes(){
            const { data } = await axios.get(`/api/recipe/recipes/${id}`)
            setRecipe(data)
        }
        fetchRecipes()
        }, [id])

    return(
        <div>

            <Button as={Link} to="/">Go Back</Button>

            <Row style={{ marginTop: '20px' }} className="justify-content-center">
                <Col md={5}>
                    <Image src={recipe.image} alt={recipe.title} fluid />
                </Col>

                <Col md={3}>
                    <ListGroup variant="flush">
                        <ListGroup.Item>
                            <h3>{recipe.title}</h3>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <Rating value={recipe.rating} text={`${recipe.numComments} comments`} color={'#f8e825'} />
                        </ListGroup.Item>

                        <ListGroup.Item>
                            Price: <strong>  ${recipe.price} </strong>
                        </ListGroup.Item>
                        <ListGroup.Item>
                            Time: <strong> {recipe.time_minutes} min. </strong>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            Description: {recipe.description}
                        </ListGroup.Item>
                    </ListGroup>

                    <br></br>

                {/* Ingredients Section */}
                {/* <Row style={{ marginTop: '20px' }}> */}
                        <Col md={10}>
                            <Card>
                                <Card.Body>
                                    <Card.Title>Ingredients</Card.Title>
                                    <ListGroup variant="flush">
                                        {recipe.ingredients && recipe.ingredients.length > 0 ? (
                                            recipe.ingredients.map((ingredient) => (
                                                <ListGroup.Item key={ingredient.id}>
                                                    {ingredient.name}
                                                </ListGroup.Item>
                                            ))
                                        ) : (
                                            <ListGroup.Item>No ingredients listed for this recipe.</ListGroup.Item>
                                        )}
                                    </ListGroup>
                                </Card.Body>
                            </Card>
                        </Col>
                    {/* </Row> */}
                    <br></br>
                    <Col md={10}>
                            <ListGroup>

                                </ListGroup>

                                <ListGroup.Item>
                                    <Button
                                        // onClick={addToCartHandler}
                                        className='btn-block'
                                        disabled={recipe.countInStock == 0}
                                        type='button'>
                                        Save
                                    </Button>
                                </ListGroup.Item>

                    </Col>
                </Col>
            </Row>

        </div>
    );
}

export default RecipeScreen