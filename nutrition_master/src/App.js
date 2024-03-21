// import React, {useState, useEffect} from 'react';
import jsonData from './meal_data.json';
import './App.scss';
import { Doughnut } from 'react-chartjs-2';
import 'chart.js/auto';


const GaugeChart = ({ score }) => {
    const data = {
        datasets: [
            {
                data: [score, 100 - score], // Assume the total score is 100
                backgroundColor: ['#00B855', '#535353'],
                borderWidth: 0,
            },
        ],
    };

    const options = {
        // rotation: Math.PI,
        // circumference: Math.PI,
        responsive: true,
        maintainAspectRatio: false,
        cutout: '75%',
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                enabled: false,
            },
        },
    };

    return <div className="gauge-container">
            <Doughnut data={data} options={options} />
            <div className="gauge-container_flow">
                <div className="gauge-container_flow_text">Today's score</div>
                <div className="gauge-container_flow_score">{score}</div>
                <div className="gauge-container_flow_assessment">Great</div>
            </div>
        </div>
};


function App() {
    const macrosString = jsonData[jsonData.length - 1].Meal.Dish1["Macros (Protein/Carbs/Fats)"];
    const macrosArray = macrosString.split('/');
    // Your stats data here
    const stats = {
        score: 71,
        time: new Date(jsonData[jsonData.length - 1].Time).toLocaleDateString('en-CA'),
        dishName: jsonData[jsonData.length - 1].Meal.Dish1.Dishname,
        weight: parseInt(jsonData[jsonData.length - 1].Meal.Dish1.Weight, 10),
        calories: parseInt(jsonData[jsonData.length - 1].Meal.Dish1.Calories, 10),
        macros: {
            proteins: parseInt(macrosArray[0].split('g')[0], 10),
            carbs: parseInt(macrosArray[1].split('g')[0], 10),
            fats: parseInt(macrosArray[2].split('g')[0], 10),
        }
        // Other stats...
    };

    return (
        <div>
            <h1>Meal Data Review</h1>
            <div className="container">
                <p>Time: {stats.time}</p>
                <GaugeChart score={stats.score}/>
                <div className="container_details">
                   <div className="container_details_title">DISH</div>
                    <div className="container_details_desc" style={{backgroundColor: '#00B855'}}><strong>DishName: </strong>{stats.dishName}</div>

                    <div className="container_details_title">WEIGHT</div>
                    <div className="container_details_desc" style={{backgroundColor: '#FFDB1D'}}><strong>Weight: </strong>{stats.weight}</div>

                    <div className="container_details_title">CALORIES</div>
                    <div className="container_details_desc" style={{backgroundColor: '#FF3D00'}}><strong>Calories: </strong>{stats.calories}</div>

                    <div className="container_details_title">MACROS</div>
                    <div className="container_details_desc" style={{backgroundColor: '#0080ff'}}><strong>Proteins: </strong>{stats.macros.proteins}</div>
                    <div className="container_details_desc" style={{backgroundColor: '#0080ff'}}><strong>Carbs: </strong>{stats.macros.carbs}</div>
                    <div className="container_details_desc" style={{backgroundColor: '#0080ff'}}><strong>Fats: </strong>{stats.macros.fats}</div>
                </div>
                <ul>
                {/*    /!*{jsonData.map((meal, index) => (*!/*/}
                {/*    /!*    <li key={index}>*!/*/}
                {/*    /!*        <p>Time: {meal.Time}</p>*!/*/}
                {/*    /!*        <p>Dishname: {meal.Meal.Dish1.Dishname}</p>*!/*/}
                {/*    /!*        <p>Weight: {meal.Meal.Dish1.Weight}</p>*!/*/}
                {/*    /!*        <p>Calories: {meal.Meal.Dish1.Calories}</p>*!/*/}
                {/*    /!*        <p>Macros: {meal.Meal.Dish1["Macros (Protein/Carbs/Fats)"]}</p>*!/*/}
                {/*    /!*        <p>Ingredients: {meal.Meal.Dish1.Ingredients}</p>*!/*/}
                {/*    /!*    </li>*!/*/}
                {/*    /!*))}*!/*/}
                {/*    {jsonData.length > 0 && (*/}
                {/*        <li>*/}
                {/*            <p>Time: {jsonData[jsonData.length - 1].Time}</p>*/}
                {/*            <p>Dishname: {jsonData[jsonData.length - 1].Meal.Dish1.Dishname}</p>*/}
                {/*            <p>Weight: {jsonData[jsonData.length - 1].Meal.Dish1.Weight}</p>*/}
                {/*            <p>Calories: {jsonData[jsonData.length - 1].Meal.Dish1.Calories}</p>*/}
                {/*            <p>Macros (Protein/Carbs/Fats): {jsonData[jsonData.length - 1].Meal.Dish1["Macros (Protein/Carbs/Fats)"]}</p>*/}
                {/*            /!*<p>Ingredients: {jsonData[jsonData.length - 1].Meal.Dish1.Ingredients}</p>*!/*/}
                {/*        </li>*/}
                {/*    )}*/}

                </ul>
            </div>

        </div>
    );
}

export default App;
