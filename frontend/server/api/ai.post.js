export default defineEventHandler(async (event) => {
  console.log('✅ API /api/ai called');
  
  try {
    const body = await readBody(event);
    console.log('📦 Received body:', body);

    const { productDetails, productData } = body;
    const dataToProcess = productDetails || productData;

    if (!dataToProcess) {
      throw createError({
        statusCode: 400,
        message: 'No product data received'
      });
    }

    // TODO: Add your AI processing here
    // For now, just return the cleaned data
    const result = {
      success: true,
      productData: dataToProcess, // Return the actual text from n8n
      summary: `ได้รับข้อมูล ${dataToProcess.length} ตัวอักษร`,
      timestamp: new Date().toISOString()
    };

    console.log('✅ Sending response');
    return result;

  } catch (error) {
    console.error('❌ API Error:', error);
    throw createError({
      statusCode: error.statusCode || 500,
      message: error.message || 'Internal server error'
    });
  }
});