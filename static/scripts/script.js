"use strict"
$(document).ready(() => {
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


    const handleSelect = (selected) => {
      switch (selected) {
          case 'first': {
            handleStarSelect(1);
            break
          }
          case 'second': {
            handleStarSelect(2);
            break
          }
          case 'third': {
            handleStarSelect(3);
            break
          }
          case 'fourth': {
            handleStarSelect(4);
            break
          }
          case 'fifth': {
            handleStarSelect(5);
            break
          }
      }
    }

    const handleStarSelect = (size) => {
        const children = document.querySelector('#rating_form').children
        for (let i = 0; i < children.length; i++) {
            if (i <= size) {
                children[i].classList.add('checked')
            } else {
                children[i].classList.remove('checked')
            }
        }
    }

    const getRatingValue = (stringValue) => {
        let number;
        if (stringValue === 'first') number = 1
        else if (stringValue === 'second') number = 2
        else if (stringValue === 'third') number = 3
        else if (stringValue === 'fourth') number = 4
        else if (stringValue === 'fifth') number = 5
        else number = 0
        return number
    }

    const one = document.getElementById('first')
    const two = document.getElementById('second')
    const three = document.getElementById('third')
    const four = document.getElementById('fourth')
    const five = document.getElementById('fifth')

    const array = [one, two, three, four, five]
    const rating_form = document.getElementById('rating_form')

    if (array) {
        array.forEach(item => item.addEventListener('mouseover', (event) => {
        handleSelect(event.target.id);
        }))

        rating_form.addEventListener('mouseleave', (event) => {
            for (let i = 1; i < rating_form.children.length; i++)
                rating_form.children[i].classList.remove('checked')
        })

        array.forEach(item => item.addEventListener('click', (event) => {
            const value = event.target.id
            rating_form.addEventListener('submit', (e) => {
                event.preventDefault()
                const user_id = e.target.name
                const rating_value = getRatingValue(value)


                    $.ajax({
                        url: `http://127.0.0.1:8000/date/profile/${user_id}/rate`,
                        type: 'post',
                        headers: {
                            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
                        },
                        data: {
                            'user_id': user_id,
                            'rating_value': rating_value,
                        },
                        success: (response) => {
                            console.log(response)
                        },
                        error: (error) => {
                            console.log(error)
                        }
                    })
            })
        }))
    }
})

