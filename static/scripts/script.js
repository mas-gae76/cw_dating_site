"use strict"

const ratings = document.querySelectorAll('.rating')
if (ratings.length > 0) initRatings()

function initRatings() {
    for (let i = 0; i < ratings.length; i++) initRating(ratings[i])
}
function initRating(rating) {
    let ratingValue = rating.querySelector('.rating_value').innerHTML
    let ratingActive = rating.querySelector('.rating_active')
    const ratingActiveWidth = ratingValue / 0.05
    ratingActive.style.width = `${ratingActiveWidth}%`
}
















// const handleSelect = (selected) => {
//   switch (selected) {
//       case 'first': {
//         handleStarSelect(0);
//         break
//       }
//       case 'second': {
//         handleStarSelect(1);
//         break
//       }
//       case 'third': {
//         handleStarSelect(2);
//         break
//       }
//       case 'fourth': {
//         handleStarSelect(3);
//         break
//       }
//       case 'fifth': {
//         handleStarSelect(4);
//         break
//       }
//   }
// }
//
// const handleStarSelect = (size) => {
//     const children = document.getElementById('rating').children
//     for (let i = 0; i < children.length; i++) {
//         if (i <= size) {
//             children[i].classList.add('checked')
//         } else {
//             children[i].classList.remove('checked')
//         }
//     }
// }
// const rating = document.querySelector('.rating')
// const one = document.getElementById('first')
// const two = document.getElementById('second')
// const three = document.getElementById('third')
// const four = document.getElementById('fourth')
// const five = document.getElementById('fifth')
//
// const array = [one, two, three, four, five]


// rating.children.forEach(item => item.addEventListener('mouseover', (event) =>{
//     handleSelect(event.target.id);

    // array.forEach(item => item.addEventListener('click', (event) => {
    //     const value = event.target.id
    //     alert(value)
    // }))
