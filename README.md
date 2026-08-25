# Bailey Electrical Website

A modern, responsive electrician website built with HTML, Tailwind CSS, and Calendly integration.

## Features

- 🎨 Modern, professional design with Tailwind CSS
- 📱 Fully responsive (mobile, tablet, desktop)
- 🗓️ Calendly integration for easy appointment booking
- ⚡ Fast loading with CDN resources
- 🎯 Service showcase sections
- ⭐ Testimonials section
- 📧 Contact information
- 🔗 Social media links
- 🌙 Professional color scheme (slate, amber, gray)

## Getting Started

### Option 1: Open Directly in Browser
1. Open `index.html` in your web browser
2. Click "Book Now" or "Schedule Your Free Consultation" to test Calendly

### Option 2: Use a Local Server
For best results, serve the file through a local web server:

```bash
# Using Python 3
python -m http.server 8000

# Using Node.js (http-server)
npx http-server

# Using PHP
php -S localhost:8000
```

Then visit: `http://localhost:8000`

## Customization

### Update Calendly Link
Replace the placeholder Calendly URL in the modal section:
- Find: `data-url="https://calendly.com/baileyelectrical"`
- Replace with your actual Calendly link

### Update Phone Number
Update the phone number:
- Find: `07590 275205`
- Replace with the actual phone number

### Update Email
Update the email address:
- Find: `baileyelectrical.mb@gmail.com`
- Replace with the actual email

### Update Facebook Link
The Facebook link is already set but can be updated:
- Find: `https://www.facebook.com/profile.php?id=61591179188922`
- Replace with your page URL if needed

### Change Colors
Main colors are:
- **Primary**: Slate-900 (dark navy)
- **Accent**: Amber-500 (gold/orange)
- **Background**: Gray-50 (light gray)

To change colors, search and replace color classes:
- `bg-slate-900` → your primary color
- `bg-amber-500` → your accent color
- `text-amber-600` → accent text color

### Update Images
Images are from Unsplash. To use custom images, replace the URLs:
- Professional Electrician: `https://images.unsplash.com/photo-1621905167918-48416bd8575a`
- Expert Team: `https://images.unsplash.com/photo-1619983081575-430f63602fbb`

### Update Copy/Text
All text content can be easily edited. Key sections:
- Hero title and description
- Service descriptions
- About section text
- Testimonials
- Contact information

## Deployment

### Deploy to GitHub Pages
1. Create a GitHub repository
2. Upload `index.html` to the repository
3. Go to Settings → Pages → Select main branch as source
4. Your site will be live at `https://yourusername.github.io/bailey-electrical`

### Deploy to Netlify
1. Drag and drop the `index.html` file to Netlify
2. Or connect your GitHub repository for auto-deploys

### Deploy to Vercel
1. Import your GitHub repository to Vercel
2. Vercel will automatically detect and deploy

### Host on Your Own Server
1. Upload `index.html` to your web hosting
2. Ensure your hosting supports HTML files

## Dependencies

All dependencies are loaded via CDN:
- **Tailwind CSS** - Styling
- **Font Awesome** - Icons
- **Calendly Widget** - Appointment booking

No build process or installation required!

## Browser Support

Works on all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Performance Tips

1. The page uses CDN resources for fast loading
2. Images are optimized from Unsplash
3. No JavaScript frameworks needed
4. Minimal inline styles for maximum performance

## SEO Optimization

The page includes:
- Semantic HTML structure
- Meta tags and title
- Proper heading hierarchy
- Alt text for images

## Future Enhancements

Consider adding:
- Contact form with email notifications
- Photo gallery of completed projects
- Blog section
- Service area map
- Customer portal
- Appointment reminders

## Support

For questions or issues with Calendly integration:
1. Visit: https://calendly.com/features/embed
2. Generate your embed code
3. Replace the `data-url` attribute in the modal

---

**Built for Bailey Electrical - Professional Electrical Services in Cardiff & South Wales**
