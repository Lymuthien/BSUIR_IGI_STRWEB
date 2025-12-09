require('dotenv').config();
const mongoose = require('mongoose');
const connectDB = require('../config/database');
const { User, Estate, Service, ServiceCategory, Review } = require('../models');

connectDB();

const seedData = async () => {
  try {
    await User.deleteMany({});
    await Estate.deleteMany({});
    await Service.deleteMany({});
    await ServiceCategory.deleteMany({});
    await Review.deleteMany({});

    console.log('Cleared existing data...');

    // Create service categories
    const categories = await ServiceCategory.insertMany([
      { name: 'Apartment' },
      { name: 'House' },
      { name: 'Commercial' },
      { name: 'Land' }
    ]);
    console.log('Created service categories...');

    // Create services
    const services = await Service.insertMany([
      {
        name: 'Apartment Sale',
        category: categories[0]._id,
        cost: 5000
      },
      {
        name: 'House Sale',
        category: categories[1]._id,
        cost: 7000
      },
      {
        name: 'Commercial Property Sale',
        category: categories[2]._id,
        cost: 10000
      },
      {
        name: 'Land Sale',
        category: categories[3]._id,
        cost: 3000
      }
    ]);
    console.log('Created services...');

    // Create users 
    const admin = await User.create({
      username: 'admin',
      email: 'admin@agency.com',
      password: 'admin123',
      firstName: 'Admin',
      lastName: 'User',
      role: 'admin',
      phoneNumber: '+375(29)123-45-67',
      birthDate: new Date('1990-01-01')
    });

    const employee1 = await User.create({
      username: 'employee1',
      email: 'employee1@agency.com',
      password: 'emp123',
      firstName: 'John',
      lastName: 'Doe',
      role: 'employee',
      phoneNumber: '+375(29)234-56-78',
      birthDate: new Date('1985-05-15')
    });

    const client1 = await User.create({
      username: 'client1',
      email: 'client1@example.com',
      password: 'client123',
      firstName: 'Jane',
      lastName: 'Smith',
      role: 'client',
      phoneNumber: '+375(29)345-67-89',
      birthDate: new Date('1992-08-20')
    });

    const client2 = await User.create({
      username: 'client2',
      email: 'client2@example.com',
      password: 'client123',
      firstName: 'Bob',
      lastName: 'Johnson',
      role: 'client',
      phoneNumber: '+375(29)456-78-90',
      birthDate: new Date('1988-12-10')
    });

    const users = [admin, employee1, client1, client2];
    console.log('Created users...');

    // Create estates 
    const estates = await Estate.insertMany([
      {
        address: 'Minsk, Independence Avenue 10, Apt. 25',
        cost: 95000,
        area: 65,
        category: services[0]._id,
        description: 'Spacious 2-room apartment in the city center. Recently renovated. Modern kitchen and bathroom. Balcony with city view.',
        rooms: 2,
        floor: 5,
        totalFloors: 9,
        status: 'available',
        createdBy: employee1._id
      },
      {
        address: 'Minsk, Pobediteley Avenue 30, Apt. 12',
        cost: 120000,
        area: 80,
        category: services[0]._id,
        description: 'Luxurious 3-room apartment with panoramic windows. High-quality renovation. Near metro station.',
        rooms: 3,
        floor: 8,
        totalFloors: 12,
        status: 'available',
        createdBy: employee1._id
      },
      {
        address: 'Minsk, Gikalo Street 5, Apt. 7',
        cost: 75000,
        area: 50,
        category: services[0]._id,
        description: 'Cozy 1-room apartment in a quiet area. Ideal for young professionals or as an investment.',
        rooms: 1,
        floor: 3,
        totalFloors: 5,
        status: 'available',
        createdBy: employee1._id
      },
      {
        address: 'Minsk, Pushkin Avenue 45, Apt. 18',
        cost: 135000,
        area: 95,
        category: services[0]._id,
        description: 'Large 4-room apartment with two balconies. Designer renovation. Spacious living room and bedrooms.',
        rooms: 4,
        floor: 6,
        totalFloors: 10,
        status: 'available',
        createdBy: employee1._id
      },
      {
        address: 'Minsk, Dzerzhinsky Avenue 120, House',
        cost: 250000,
        area: 150,
        category: services[1]._id,
        description: 'Beautiful two-story house with garden. Modern architecture. Garage included. Perfect for families.',
        rooms: 5,
        status: 'available',
        createdBy: employee1._id
      },
      {
        address: 'Minsk, Rokossovsky Avenue 55, House',
        cost: 180000,
        area: 120,
        category: services[1]._id,
        description: 'Charming one-story house with large plot. Well-maintained. Near forest. Peaceful location.',
        rooms: 4,
        status: 'available',
        createdBy: employee1._id
      },
      {
        address: 'Minsk, Partisan Avenue 80, Commercial Space',
        cost: 350000,
        area: 200,
        category: services[2]._id,
        description: 'Prime commercial space in busy area. High foot traffic. Suitable for retail or office.',
        status: 'available',
        createdBy: employee1._id
      },
      {
        address: 'Minsk, Minsk District, Land Plot',
        cost: 45000,
        area: 500,
        category: services[3]._id,
        description: 'Large land plot for construction. All utilities available. Beautiful location near lake.',
        status: 'available',
        createdBy: employee1._id
      },
      {
        address: 'Minsk, Bogdanovich Street 15, Apt. 9',
        cost: 88000,
        area: 58,
        category: services[0]._id,
        description: 'Modern 2-room apartment with Euro renovation. Open kitchen-living area. Quiet courtyard.',
        rooms: 2,
        floor: 4,
        totalFloors: 7,
        status: 'available',
        createdBy: employee1._id
      },
      {
        address: 'Minsk, Nezavisimosti Avenue 100, Apt. 42',
        cost: 165000,
        area: 110,
        category: services[0]._id,
        description: 'Premium 4-room apartment with luxury finish. Two bathrooms. Large balcony. City center location.',
        rooms: 4,
        floor: 10,
        totalFloors: 15,
        status: 'available',
        createdBy: employee1._id
      },
      {
        address: 'Minsk, Vitebsk Highway 25, House',
        cost: 220000,
        area: 140,
        category: services[1]._id,
        description: 'Spacious family house with modern design. Large kitchen, living room with fireplace. Private garden.',
        rooms: 5,
        status: 'available',
        createdBy: employee1._id
      },
      {
        address: 'Minsk, Leningradskaya Street 20, Apt. 33',
        cost: 72000,
        area: 48,
        category: services[0]._id,
        description: 'Compact 1-room apartment for sale. Good condition. Near public transport. Affordable price.',
        rooms: 1,
        floor: 7,
        totalFloors: 9,
        status: 'available',
        createdBy: employee1._id
      }
    ]);
    console.log('Created estates...');

    // Create reviews
    await Review.insertMany([
      {
        user: client1._id,
        rating: 5,
        text: 'Excellent service! The agent was very professional and helped me find the perfect apartment.',
        estate: estates[0]._id
      },
      {
        user: client2._id,
        rating: 4,
        text: 'Good experience overall. Quick response and helpful staff.',
        estate: estates[1]._id
      }
    ]);
    console.log('Created reviews...');

    console.log('\nSeed data created successfully!');
    console.log(`Created: ${categories.length} categories, ${services.length} services, ${users.length} users, ${estates.length} estates`);
    
    process.exit(0);
  } catch (error) {
    console.error('Error seeding data:', error);
    process.exit(1);
  }
};

seedData();

