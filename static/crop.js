function openNav() {
    document.getElementById("mySidebar").style.width = "300px";
  }
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
  }
  document.getElementById("servicesLink").addEventListener("click", openNav);


  const countries = ['Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia',
    'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
    'Bangladesh', 'Belarus', 'Belgium', 'Botswana', 'Brazil',
    'Bulgaria', 'Burkina Faso', 'Burundi', 'Cameroon', 'Canada',
    'Central African Republic', 'Chile', 'Colombia', 'Croatia',
    'Denmark', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
    'Eritrea', 'Estonia', 'Finland', 'France', 'Germany', 'Ghana',
    'Greece', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras',
    'Hungary', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Italy',
    'Jamaica', 'Japan', 'Kazakhstan', 'Kenya', 'Latvia', 'Lebanon',
    'Lesotho', 'Libya', 'Lithuania', 'Madagascar', 'Malawi',
    'Malaysia', 'Mali', 'Mauritania', 'Mauritius', 'Mexico',
    'Montenegro', 'Morocco', 'Mozambique', 'Namibia', 'Nepal',
    'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Norway',
    'Pakistan', 'Papua New Guinea', 'Peru', 'Poland', 'Portugal',
    'Qatar', 'Romania', 'Rwanda', 'Saudi Arabia', 'Senegal',
    'Slovenia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan',
    'Suriname', 'Sweden', 'Switzerland', 'Tajikistan', 'Thailand',
    'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 'United Kingdom',
    'Uruguay', 'Zambia', 'Zimbabwe']

    const countryOptions = document.getElementById("countryOptions");
    countries.forEach(country => {
        const option = document.createElement("option");
        option.value = country;
        countryOptions.appendChild(option);
    });


    