import React, { useState, useEffect } from 'react';
import jsonData from './meal_data.json';

function App() {
  return (
    <div>
      <h1>Meal Data</h1>
      <ul>
        {jsonData.map((meal, index) => (
          <li key={index}>
            <p>Time: {meal.Time}</p>
            <p>Dishname: {meal.Meal.Dish1.Dishname}</p>
            <p>Weight: {meal.Meal.Dish1.Weight}</p>
            <p>Calories: {meal.Meal.Dish1.Calories}</p>
            <p>Macros: {meal.Meal.Dish1["Macros (Protein/Carbs/Fats)"]}</p>
            <p>Ingredients: {meal.Meal.Dish1.Ingredients}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
export default App;
