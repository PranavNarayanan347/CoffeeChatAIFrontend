# Stripe Subscription Setup Guide

This guide will help you set up Stripe payments for CoffeeChat AI with a $15/month subscription and 7-day free trial.

## Prerequisites

- Stripe account (sign up at https://stripe.com)
- Stripe API keys (Publishable Key and Secret Key)

## Step 1: Get Your Stripe Keys

1. Log in to your [Stripe Dashboard](https://dashboard.stripe.com)
2. Go to **Developers** → **API keys**
3. Copy your **Publishable key** (starts with `pk_test_` or `pk_live_`)
4. Copy your **Secret key** (starts with `sk_test_` or `sk_live_`)

⚠️ **Important**: Use test keys (`pk_test_`/`sk_test_`) for development, and live keys (`pk_live_`/`sk_live_`) for production.

## Step 2: Set Up Environment Variables

### For Development (Windows)

Create a `.env` file in the `backend` directory or set environment variables:

```bash
# Stripe Configuration
STRIPE_SECRET_KEY_TEST=sk_test_your_secret_key_here
STRIPE_PRICE_ID=price_xxxxx  # Will be generated in next step
```

### For Production

```bash
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PRICE_ID=price_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx  # For webhook verification
```

## Step 3: Get or Create Price ID

You have a Product ID (`prod_TbjNIPCwvMGBX6`), but we need a **Price ID** for subscriptions.

### Option A: Use the Helper Script (Recommended)

Run the setup script to automatically find or create the price:

```bash
cd backend
python scripts/setup_stripe_price.py
```

The script will:
- Check if a $15/month price already exists for your product
- Create one if it doesn't exist
- Display the Price ID to use

### Option B: Manual Setup via Stripe Dashboard

1. Go to [Stripe Dashboard](https://dashboard.stripe.com) → **Products**
2. Click on your product (`prod_TbjNIPCwvMGBX6`)
3. If a price already exists:
   - Click on the price
   - Copy the **Price ID** (starts with `price_`)
4. If no price exists:
   - Click **"Add another price"**
   - Set amount to **$15.00**
   - Set billing period to **Monthly**
   - Click **"Add price"**
   - Copy the **Price ID**

### Option C: Create Price via Stripe API

You can also create the price programmatically:

```python
import stripe
import os

stripe.api_key = os.environ["STRIPE_SECRET_KEY_TEST"]

price = stripe.Price.create(
    product="prod_TbjNIPCwvMGBX6",
    unit_amount=1500,  # $15.00 in cents
    currency='usd',
    recurring={'interval': 'month'},
    nickname='Monthly Subscription - $15',
)

print(f"Price ID: {price.id}")
```

## Step 4: Configure Webhook (For Production)

Webhooks allow Stripe to notify your backend when subscription events occur.

### Development (Using Stripe CLI)

1. Install [Stripe CLI](https://stripe.com/docs/stripe-cli)
2. Login: `stripe login`
3. Forward webhooks to local server:
   ```bash
   stripe listen --forward-to http://localhost:5000/api/subscription/webhook
   ```
4. Copy the webhook signing secret (starts with `whsec_`)
5. Set it as: `export STRIPE_WEBHOOK_SECRET=whsec_...`

### Production

1. Go to [Stripe Dashboard](https://dashboard.stripe.com) → **Developers** → **Webhooks**
2. Click **"Add endpoint"**
3. Set endpoint URL: `https://yourdomain.com/api/subscription/webhook`
4. Select events to listen for:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
5. Copy the **Signing secret** (starts with `whsec_`)
6. Set it as environment variable: `STRIPE_WEBHOOK_SECRET=whsec_...`

## Step 5: Test the Integration

1. **Start your backend server**:
   ```bash
   cd backend
   python app.py
   ```

2. **Start your frontend**:
   ```bash
   npm run dev
   ```

3. **Test the checkout flow**:
   - Go to the landing page
   - Click "Start Free Trial"
   - Complete the checkout (use test card: `4242 4242 4242 4242`)
   - Verify subscription appears in your Profile page

## Test Cards

Use these test card numbers in Stripe test mode:

- **Success**: `4242 4242 4242 4242`
- **Requires authentication**: `4000 0025 0000 3155`
- **Declined**: `4000 0000 0000 0002`

Use any future expiry date, any CVC, and any ZIP code.

## Troubleshooting

### "Stripe price ID not configured" error

- Make sure `STRIPE_PRICE_ID` is set in your environment
- Verify the Price ID is correct (starts with `price_`)
- Check that the price is active in Stripe Dashboard

### Webhook not working

- Verify webhook URL is accessible
- Check webhook signing secret matches
- View webhook logs in Stripe Dashboard → Developers → Webhooks

### Subscription not appearing after checkout

- Check webhook logs in Stripe Dashboard
- Verify webhook endpoint is receiving events
- Check backend logs for errors

## Environment Variables Summary

```bash
# Required
STRIPE_SECRET_KEY_TEST=sk_test_...  # or STRIPE_SECRET_KEY for production
STRIPE_PRICE_ID=price_...

# Optional (for webhook verification)
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Next Steps

- ✅ Set up Stripe keys
- ✅ Create/get Price ID
- ✅ Configure webhook (for production)
- ✅ Test checkout flow
- ✅ Monitor subscriptions in Stripe Dashboard

For more information, see:
- [Stripe Documentation](https://stripe.com/docs)
- [Stripe Testing Guide](https://stripe.com/docs/testing)



