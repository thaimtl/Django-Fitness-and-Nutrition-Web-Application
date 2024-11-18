document.addEventListener("DOMContentLoaded", function() {
  // Background images for the index page
  if (document.getElementById("index-page")) {
      const images = backgroundImages;
      let currentIndex = 0;
      const backgroundDiv = document.querySelector(".background");

      function changeBackground() {
          backgroundDiv.style.backgroundImage = `url(${images[currentIndex]})`;
          currentIndex = (currentIndex + 1) % images.length;
      }

      setInterval(changeBackground, 5000); 
      changeBackground(); 
  }

  // Form submission for the profile page
  const profileForm = document.getElementById('profile-form');
  const updateButton = document.getElementById('update-button');
  const successMessage = document.getElementById('success-message');

  profileForm.addEventListener('submit', function(event) {
      event.preventDefault(); 

      const formData = new FormData(profileForm);

      fetch(profileForm.action, {
          method: 'POST',
          body: formData,
          headers: {
              'X-Requested-With': 'XMLHttpRequest',
          },
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              updateButton.style.display = 'none';
              successMessage.style.display = 'block';
          } else {
              console.error("Form submission failed.");
          }
      });
  });

  // Form submission for logging food
  const logFoodForm = document.getElementById('log-food-form');
  const foodLogList = document.getElementById('food-log-list');
  const totalCalories = document.getElementById('total-calories');
  const totalProtein = document.getElementById('total-protein');
  const totalCarbs = document.getElementById('total-carbs');
  const totalFats = document.getElementById('total-fats');

  logFoodForm.addEventListener('submit', function(event) {
      event.preventDefault();
      const formData = new FormData(logFoodForm);
      fetch(logFoodForm.action, {
          method: 'POST',
          body: formData,
          headers: {
              'X-Requested-With': 'XMLHttpRequest',
              'X-CSRFToken': formData.get('csrfmiddlewaretoken')
          }
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              const foodLog = data.food_log;
              const listItem = document.createElement('li');
              listItem.innerHTML = `
                  <strong>${foodLog.food_name}</strong> - ${foodLog.date_logged}<br>
                  Quantity: ${foodLog.quantity} grams<br>
                  Calories: <span class="calories">${foodLog.calories}</span><br>
                  Protein: <span class="protein">${foodLog.protein}</span> grams<br>
                  Carbs: <span class="carbs">${foodLog.carbs}</span> grams<br>
                  Fats: <span class="fats">${foodLog.fats}</span> grams<br>
                  <form method="post" action="/delete_food_log/${foodLog.id}/" class="delete-food-log-form">
                      <input type="hidden" name="csrfmiddlewaretoken" value="${formData.get('csrfmiddlewaretoken')}">
                      <button type="submit" class="btn btn-danger">Delete</button>
                  </form>
              `;
              foodLogList.prepend(listItem);

              // Update totals
              totalCalories.textContent = parseFloat(totalCalories.textContent) + foodLog.calories;
              totalProtein.textContent = parseFloat(totalProtein.textContent) + foodLog.protein;
              totalCarbs.textContent = parseFloat(totalCarbs.textContent) + foodLog.carbs;
              totalFats.textContent = parseFloat(totalFats.textContent) + foodLog.fats;

              // Reset form
              logFoodForm.reset();
          }
      });
  });

  // Delete food log
    foodLogList.addEventListener('submit', function(event) {
      if (event.target.classList.contains('delete-food-log-form')) {
          event.preventDefault();
          const form = event.target;
          const formData = new FormData(form);
          fetch(form.action, {
              method: 'POST',
              body: formData,
              headers: {
                  'X-Requested-With': 'XMLHttpRequest',
                  'X-CSRFToken': formData.get('csrfmiddlewaretoken')
              }
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  const listItem = form.closest('li');
                  const foodLog = {
                      calories: parseFloat(listItem.querySelector('.calories').textContent),
                      protein: parseFloat(listItem.querySelector('.protein').textContent),
                      carbs: parseFloat(listItem.querySelector('.carbs').textContent),
                      fats: parseFloat(listItem.querySelector('.fats').textContent)
                  };

                  // Update totals
                  totalCalories.textContent = parseFloat(totalCalories.textContent) - foodLog.calories;
                  totalProtein.textContent = parseFloat(totalProtein.textContent) - foodLog.protein;
                  totalCarbs.textContent = parseFloat(totalCarbs.textContent) - foodLog.carbs;
                  totalFats.textContent = parseFloat(totalFats.textContent) - foodLog.fats;

                  // Remove list item
                  listItem.remove();
              }
          });
      }
    });
  // Toggle add exercise form
  const addExerciseForm = document.getElementById('add-exercise-form');
  // Form submission for adding exercise
  const addExercise = document.getElementById('add-exercise');
  addExercise.addEventListener('submit', function(event) {
      event.preventDefault();
      const formData = new FormData(addExercise);
      fetch(addExercise.action, {
          method: 'POST',
          body: formData,
          headers: {
              'X-Requested-With': 'XMLHttpRequest',
              'X-CSRFToken': formData.get('csrfmiddlewaretoken')
          }
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              const workoutPlan = data.workout_plan;
              const workoutDiv = document.createElement('div');
              workoutDiv.classList.add('workout');
              workoutDiv.innerHTML = `
                  <h2>${workoutPlan.name_of_exercise.toUpperCase()}</h2>
                  <p><strong>Sets:</strong> ${workoutPlan.sets}</p>
                  <p><strong>Reps:</strong> ${workoutPlan.reps}</p>
                  <p><strong>Description:</strong> <a href="${workoutPlan.description}" target="_blank">${workoutPlan.description}</a></p>
                  <form method="post" action="/remove_exercise/${workoutPlan.id}/" class="delete-exercise-form">
                      <input type="hidden" name="csrfmiddlewaretoken" value="${formData.get('csrfmiddlewaretoken')}">
                      <button type="submit" class="btn btn-danger">Remove</button>
                  </form>
              `;
              document.querySelector('.my-workout-plan').appendChild(workoutDiv);
              addExercise.reset();
              addExerciseForm.style.display = 'block';

              // Add event listener for the new remove button
              workoutDiv.querySelector('.delete-exercise-form').addEventListener('submit', function(event) {
                  event.preventDefault();
                  const formData = new FormData(this);
                  fetch(this.action, {
                      method: 'POST',
                      body: formData,
                      headers: {
                          'X-Requested-With': 'XMLHttpRequest',
                          'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                      }
                  }).then(response => response.json())
                  .then(data => {
                      if (data.success) {
                         workoutDiv.remove(); 
                      } else {
                          console.error("Failed to remove exercise.");
                      }
                  });
              });
          } else {
              console.error("Form submission failed.");
          }
      });
  });

  // Remove exercise
  document.querySelectorAll('.delete-exercise-form').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                this.closest('.workout').remove();
            } else {
                console.error("Failed to remove exercise.");
            }
        });
    });
    });
    // Remove link for Abs Workout
    document.querySelectorAll('.delete-link-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.closest('li').remove(); // Remove the link list item from the DOM
                } else {
                    console.error("Failed to remove link.");
                }
            });
        });
    });
});
