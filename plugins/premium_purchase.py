# Premium Purchase Flow Handler
# Handles interactive premium purchase with UPI payment

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import PREMIUM_PLANS, UPI_ID, PAYMENT_QR, PAYMENT_ADMIN, OWNER_ID

#===============================================================#

@Client.on_callback_query(filters.regex("^get_premium$"))
async def get_premium_callback(client: Client, callback_query: CallbackQuery):
    """Show premium purchase options"""
    await callback_query.answer()
    
    premium_text = (
        "🌟 **Choose Payment Method** 🌟\n\n"
        "Select how you would like to pay for premium access:"
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 UPI Payment", callback_data="upi_payment")],
        [InlineKeyboardButton("« Back", callback_data="close")]
    ])
    
    await callback_query.message.edit_text(
        premium_text,
        reply_markup=keyboard
    )

#===============================================================#

@Client.on_callback_query(filters.regex("^upi_payment$"))
async def upi_payment_callback(client: Client, callback_query: CallbackQuery):
    """Show UPI payment plans"""
    await callback_query.answer()
    
    plans_text = (
        "🌟 **Choose a UPI Payment Plan** 🌟\n\n"
        "Select the plan that suits your needs:"
    )
    
    # Create buttons for each plan
    keyboard = []
    for days, price in sorted(PREMIUM_PLANS.items()):
        if days == 7:
            label = f"7 Days - ₹{price}"
        elif days == 15:
            label = f"15 Days - ₹{price}"
        elif days == 30:
            label = f"30 Days - ₹{price}"
        elif days == 180:
            label = f"6 Months - ₹{price}"
        elif days == 365:
            label = f"12 Months - ₹{price}"
        else:
            label = f"{days} Days - ₹{price}"
        
        keyboard.append([InlineKeyboardButton(label, callback_data=f"plan_{days}")])
    
    keyboard.append([InlineKeyboardButton("« Back", callback_data="get_premium")])
    
    await callback_query.message.edit_text(
        plans_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

#===============================================================#

@Client.on_callback_query(filters.regex("^plan_"))
async def plan_selected_callback(client: Client, callback_query: CallbackQuery):
    """Show payment details with QR code"""
    await callback_query.answer()
    
    # Extract plan duration from callback data
    days = int(callback_query.data.split("_")[1])
    price = PREMIUM_PLANS.get(days, 0)
    
    # Format plan name
    if days == 7:
        plan_name = "7 Days"
    elif days == 15:
        plan_name = "15 Days"
    elif days == 30:
        plan_name = "30 Days"
    elif days == 180:
        plan_name = "6 Months"
    elif days == 365:
        plan_name = "12 Months"
    else:
        plan_name = f"{days} Days"
    
    payment_text = (
        f"💳 **Payment Details for {plan_name} Premium**\n\n"
        f"• **Amount:** ₹{price}\n"
        f"• **UPI ID:** `{UPI_ID}`\n\n"
        f"**Steps to complete payment:**\n"
        f"1. Scan the QR code below or use the UPI ID\n"
        f"2. Make payment of ₹{price}\n"
        f"3. Take a screenshot of the payment\n"
        f"4. Click 'I've Made Payment' below\n"
        f"5. Send the screenshot to {PAYMENT_ADMIN}\n\n"
        f"Once payment is confirmed, your premium access will be activated."
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ I've Made Payment", callback_data=f"payment_done_{days}")],
        [InlineKeyboardButton("« Back to Plans", callback_data="upi_payment")]
    ])
    
    # Send QR code image with payment details
    try:
        await callback_query.message.delete()
        await client.send_photo(
            chat_id=callback_query.from_user.id,
            photo=PAYMENT_QR,
            caption=payment_text,
            reply_markup=keyboard
        )
    except Exception as e:
        # Fallback to text if image fails
        await callback_query.message.edit_text(
            payment_text,
            reply_markup=keyboard
        )

#===============================================================#

@Client.on_callback_query(filters.regex("^payment_done_"))
async def payment_done_callback(client: Client, callback_query: CallbackQuery):
    """Handle payment confirmation"""
    await callback_query.answer("Payment notification sent to admin!")
    
    # Extract plan duration
    days = int(callback_query.data.split("_")[2])
    price = PREMIUM_PLANS.get(days, 0)
    
    # Format plan name
    if days == 7:
        plan_name = "7 Days"
    elif days == 15:
        plan_name = "15 Days"
    elif days == 30:
        plan_name = "30 Days"
    elif days == 180:
        plan_name = "6 Months"
    elif days == 365:
        plan_name = "12 Months"
    else:
        plan_name = f"{days} Days"
    
    user = callback_query.from_user
    user_info = (
        f"📩 **New Premium Purchase Request**\n\n"
        f"👤 **User:** {user.mention}\n"
        f"🆔 **User ID:** `{user.id}`\n"
        f"📱 **Username:** @{user.username if user.username else 'None'}\n\n"
        f"💎 **Plan:** {plan_name} Premium\n"
        f"💰 **Amount:** ₹{price}\n\n"
        f"⚠️ **Action Required:**\n"
        f"Verify payment screenshot and activate premium using:\n"
        f"`/addpremium {user.id} {days} days`"
    )
    
    # Notify owner/admin
    try:
        await client.send_message(OWNER_ID, user_info)
    except Exception as e:
        client.LOGGER(__name__, client.name).warning(f"Failed to notify owner: {e}")
    
    # Confirm to user
    confirmation_text = (
        "✅ **Payment Notification Sent!**\n\n"
        f"Thank you for choosing {plan_name} Premium plan!\n\n"
        f"📸 Please send your payment screenshot to {PAYMENT_ADMIN}\n\n"
        "Your premium access will be activated once the payment is verified.\n"
        "This usually takes a few minutes."
    )
    
    await callback_query.message.edit_caption(
        caption=confirmation_text,
        reply_markup=None
    )

#===============================================================#

@Client.on_callback_query(filters.regex("^get_free_access$"))
async def get_free_access_callback(client: Client, callback_query: CallbackQuery):
    """Show free access token verification"""
    await callback_query.answer()
    
    from config import TOKEN_VALIDITY_HOURS
    from plugins.shortner import get_short
    import time
    
    user_id = callback_query.from_user.id
    
    # Generate unique token link
    token_id = f"token_{user_id}_{int(time.time())}"
    token_link = f"https://t.me/{client.username}?start={token_id}"
    
    # Create shortlink for token verification using database-loaded settings
    # Settings are loaded in bot.py from database (client.short_url, client.short_api)
    try:
        short_link = get_short(token_link, client)
        
        # Verify shortlink was actually generated (not just returned original URL)
        if short_link == token_link:
            # Shortlink generation failed, show error
            shortlink_url = getattr(client, 'short_url', 'not configured')
            await callback_query.message.edit_text(
                "❌ **Shortlink Service Error**\n\n"
                "The shortlink service is currently unavailable. "
                "Please contact the admin or try again later.\n\n"
                f"**Error:** Shortlink API ({shortlink_url}) is not responding.\n\n"
                "**Admin:** Configure shortlink via /shortner command",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="close")]])
            )
            client.LOGGER(__name__, client.name).error(f"Shortlink generation failed for token verification. URL: {shortlink_url}")
            return
            
    except Exception as e:
        client.LOGGER(__name__, client.name).error(f"Shortener failed for token: {e}")
        await callback_query.message.edit_text(
            "❌ **Error**\n\n"
            "Failed to generate verification link. Please try again later or contact admin.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="close")]])
        )
        return
    
    free_access_text = (
        f"🎁 **Get Free Access for {TOKEN_VALIDITY_HOURS} Hours**\n\n"
        f"**Steps to get free access:**\n"
        f"1. Click the 'Verify & Get Access' button below\n"
        f"2. Complete the verification process\n"
        f"3. You'll be redirected back automatically\n"
        f"4. Access will be granted for {TOKEN_VALIDITY_HOURS} hours\n\n"
        f"⏰ After {TOKEN_VALIDITY_HOURS} hours, you'll need to verify again or upgrade to premium for unlimited access."
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Verify & Get Access", url=short_link)],
        [InlineKeyboardButton("💎 Get Premium Instead", callback_data="get_premium")],
        [InlineKeyboardButton("« Back", callback_data="close")]
    ])
    
    await callback_query.message.edit_text(
        free_access_text,
        reply_markup=keyboard
    )

#===============================================================#

@Client.on_callback_query(filters.regex("^close$"))
async def close_callback(client: Client, callback_query: CallbackQuery):
    """Close the message"""
    await callback_query.answer()
    await callback_query.message.delete()
