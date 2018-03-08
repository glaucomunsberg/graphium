class Graphium::GraffitisController < ApplicationController
  before_action :set_graphium_graffiti, only: [:show, :edit, :update, :destroy]
  before_filter :authenticate_user!
  layout "inside"
  # GET /graphium/graffitis
  # GET /graphium/graffitis.json
  def index
    @graphium_graffitis = Graphium::Graffiti.all
  end

  # GET /graphium/graffitis/1
  # GET /graphium/graffitis/1.json
  def show
  end

  # GET /graphium/graffitis/new
  def new
    @graphium_graffiti = Graphium::Graffiti.new
  end

  # GET /graphium/graffitis/1/edit
  def edit
  end

  def map
    @graphium_graffitis = Graphium::Graffiti.all
  end

  # POST /graphium/graffitis
  # POST /graphium/graffitis.json
  def create
    @graphium_graffiti = Graphium::Graffiti.new(graphium_graffiti_params)

    respond_to do |format|
      if @graphium_graffiti.save
        format.html { redirect_to @graphium_graffiti, notice: 'Graffiti was successfully created.' }
        format.json { render :show, status: :created, location: @graphium_graffiti }
      else
        format.html { render :new }
        format.json { render json: @graphium_graffiti.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /graphium/graffitis/1
  # PATCH/PUT /graphium/graffitis/1.json
  def update
    respond_to do |format|
      if @graphium_graffiti.update(graphium_graffiti_params)
        format.html { redirect_to @graphium_graffiti, notice: 'Graffiti was successfully updated.' }
        format.json { render :show, status: :ok, location: @graphium_graffiti }
      else
        format.html { render :edit }
        format.json { render json: @graphium_graffiti.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /graphium/graffitis/1
  # DELETE /graphium/graffitis/1.json
  def destroy
    @graphium_graffiti.destroy
    respond_to do |format|
      format.html { redirect_to graphium_graffitis_url, notice: 'Graffiti was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_graphium_graffiti
      @graphium_graffiti = Graphium::Graffiti.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def graphium_graffiti_params
      params.require(:graphium_graffiti).permit(:city, :state, :lat, :lng, :country, :pitch, :heading, :address)
    end
end
