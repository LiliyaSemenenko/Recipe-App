import React from 'react'
import { Card } from 'react-bootstrap'
import Rating from './Rating'
import { Link } from 'react-router-dom'

function Recipe({ recipe }) {
    return (
        <Card className="my-3 p-3 rounded">
            <Link to={`/recipe/${recipe._id}`}>
                <Card.Img src={recipe.image} />
            </Link>

            <Card.Body>
                <Link to={`/recipe/${recipe._id}`}>
                    <Card.Title as="h3">
                        <strong>{recipe.name}</strong>
                    </Card.Title>
                </Link>

                <Card.Text as="div">
                    <div className="my-3">
                        {/* {recipe.rating} likes {recipe.numReviews} comments */}
                        <Rating value={recipe.rating} text={`${recipe.numComments} reviews`} color={'#f8e825'} />
                    </div>
                </Card.Text>


                <Card.Text as="div">
                    @{recipe.username}
                </Card.Text>

            </Card.Body>
        </Card>
    )
}

export default Recipe