import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col } from 'react-bootstrap'
import axios from 'axios'
import Recipe from '../components/Recipe'
// import Loader from '../components/Loader'
// import Message from '../components/Message'
// import Paginate from '../components/Paginate'
// import ProductCarousel from '../components/ProductCarousel'
// import { listRecipes } from '../actions/recipeActions'


function HomeScreen({ history }) {
    // state recipes updates with setRecipes wot useState method given the original value []
    // which will be updated
    const [recipes, setRecipes] = useState([])


    // const dispatch = useDispatch()
    // const recipeList = useSelector(state => state.recipeList)
    // const { error, loading, recipes, page, pages } = recipeList

    // let keyword = history.location.search

    useEffect(() => {
        async function fetchRecipes(){
            const { data } = await axios.get('/api/recipe/recipes/')
            setRecipes(data)
        }
        fetchRecipes()
        }, [])

    return (
        <div>
            {/* {!keyword && <ProductCarousel />} */}

            <h1>Latest Recipes</h1>

                <div>
                    <Row>
                        {recipes.map(recipe => (
                            <Col key={recipe.id} sm={12} md={6} lg={4} xl={3}>
                                <Recipe recipe={recipe} />
                            </Col>
                        ))}
                    </Row>
                </div>

        </div>
    )
}

export default HomeScreen