# Calendly Setup Guide for Bailey Electrical Website

## Quick Start with Calendly

### Step 1: Create a Calendly Account
1. Go to [calendly.com](https://calendly.com)
2. Sign up with your email
3. Set up your profile with:
   - Your name
   - Time zone
   - Service descriptions

### Step 2: Create Your Calendar Events

1. In Calendly dashboard, go to **Event Types**
2. Create events for your services, e.g.:
   - **Free Consultation** (30 min)
   - **Emergency Service Call** (1 hour)
   - **Full Inspection** (2 hours)
   - **Installation/Repair** (Varies)

3. For each event, set:
   - Duration
   - Description
   - Price (if applicable)
   - Calendar connection
   - Availability

### Step 3: Get Your Embed Link

1. In the Calendly dashboard, click on **Share**
2. Select your event type (e.g., "All events")
3. Copy the link under "Embed"
4. It will look like: `https://calendly.com/youremail/event-name`

### Step 4: Update Your Website

Open `index.html` and find this line (around line 320):
```html
<div class="calendly-inline-widget" data-url="https://calendly.com/baileyelectrical" style="height:100%;"></div>
```

Replace `https://calendly.com/baileyelectrical` with your actual Calendly link:
```html
<div class="calendly-inline-widget" data-url="https://calendly.com/youremail/event-name" style="height:100%;"></div>
```

### Step 5: Test the Integration

1. Save the file
2. Open `index.html` in your browser
3. Click "Book Now" or "Schedule Your Free Consultation"
4. Verify the Calendly widget loads in the modal

## Calendly Settings Recommendations

### Availability
- Set your working hours (e.g., 9 AM - 5 PM Monday-Friday)
- Add emergency slots for after-hours availability
- Set buffer time between appointments (e.g., 15 minutes)

### Meeting Details
- Set confirmation email messages
- Add reminder emails (24 hours before)
- Customize thank you messages

### Pricing
- Mark consultations as FREE
- Add pricing for paid services if applicable
- Set payment methods if collecting deposits

### Calendar Integration
Connect Calendly to your personal calendar (Google Calendar, Outlook, etc.) so:
- Bookings sync automatically
- You don't double-book
- You have a unified schedule

### Notifications
Enable notifications so you get alerted when:
- New appointments are booked
- Appointments are cancelled
- Reminders are needed

## Testing Checklist

- [ ] Modal opens when clicking "Book Now"
- [ ] Calendly widget loads inside the modal
- [ ] Can select dates and times
- [ ] Can fill in customer information
- [ ] Confirmation email is received
- [ ] Appointment appears in your calendar
- [ ] Modal closes after booking (usually happens automatically)

## Troubleshooting

### Calendly Widget Not Loading
1. Check your `data-url` is correct
2. Clear browser cache (Ctrl+Shift+Del or Cmd+Shift+Del)
3. Try a different browser
4. Ensure you're using the public Calendly link

### Modal Not Closing After Booking
This is normal - users can close it with the X button or clicking outside

### Time Zone Issues
- Verify Calendly time zone matches your location
- Check customer's time zone in booking confirmation

### Not Receiving Notifications
- Check Calendly notification settings
- Check your email spam folder
- Verify email is correct in Calendly settings

## Advanced Customization

### Embed Custom CSS
To change the Calendly styling, add this before the closing `</body>` tag:
```html
<style>
  .calendly-inline-widget {
    background: white !important;
  }
</style>
```

### Track Booking Source
Add a UTM parameter to your link to track where bookings come from:
```
https://calendly.com/youremail/event?utm_source=website
```

### Create Booking Button
Alternative to modal - direct link button:
```html
<a href="https://calendly.com/youremail/event" target="_blank" rel="noopener noreferrer">
  Schedule Now
</a>
```

## Alternative Booking Solutions

If you want to explore other options:
- **Acuity Scheduling** - More features, pricing available
- **Setmore** - Free tier available
- **Square Appointments** - Good for service businesses
- **Bookafy** - Simple and affordable

---

## Support Resources

- **Calendly Help**: https://help.calendly.com/
- **Embed Documentation**: https://calendly.com/features/embed
- **Community Forum**: https://community.calendly.com/

## Contact Bailey Electrical

Once your site is live:
- **Phone**: 07590 275205
- **Email**: baileyelectrical.mb@gmail.com
- **Location**: Cardiff & South Wales
- **Facebook**: https://www.facebook.com/profile.php?id=61591179188922

---

**Your website is now ready to accept bookings!** 🎉
